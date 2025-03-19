#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <libgen.h>
#include <unistd.h>

int main(int argc, char *argv[])
{
    FILE *fin;
    unsigned count = 0, headersize, i;
    char *outname, *inbasename = NULL;
    if (argc != 2 && argc != 3) {
        printf("usage: unpack_cnt <SOURCE.CNT> [OUT_DIR]\n");
        return 1;
    }
    fin = fopen(argv[1], "rb");
    if (!fin) {
        printf("failed to open %s\n", argv[1]);
        return 1;
    }
    if (argc == 3) {
        struct stat outstat;
        if (stat(argv[2], &outstat) == -1) {
            if (mkdir(argv[2], S_IRWXU | S_IRWXG | S_IRWXO) == -1) {
                printf("failed to open or create %s\n", argv[2]);
                return 1;
            }
        } else if (!S_ISDIR(outstat.st_mode)) {
            printf("%s is not a folder\n", argv[2]);
            return 1;
        }
        outname = malloc(4 + 10 + 1);
        if (!outname) {
            printf("malloc failed\n");
            return 1;
        }
        if (chdir(argv[2]) == -1) {
            printf("chdir failed\n");
            return 1;
        }
    } else {
        char *dot;
        inbasename = basename(argv[1]);
        dot = strrchr(inbasename, '.');
        if (dot) *dot = '\0';
        outname = malloc(strlen(inbasename) + 4 + 10 + 1);
        if (!outname) {
            printf("malloc failed\n");
            return 1;
        }
    }
    if (fread(&count, sizeof(unsigned), 1, fin) != 1) {
        printf("failed to read file count\n");
        return 1;
    }
    headersize = (4 + count*4 + 15) & ~15;
    printf("%u entries, header size is %u\n", count, headersize);
    for (i = 0; i < count; ++i) {
        unsigned startaddr, len;
        char *buffer;
        FILE *fout;
        fseek(fin, 4 + i*4, SEEK_SET);
        if (fread(&startaddr, sizeof(unsigned), 1, fin) != 1) {
            printf("failed to read entry start address\n");
            return 1;
        }
        if (i != count-1) {
            unsigned endaddr;
            if (fread(&endaddr, sizeof(unsigned), 1, fin) != 1) {
                printf("failed to read next entry address\n");
                return 1;
            }
            len = (endaddr - startaddr)*16;
        } else {
            fseek(fin, 0, SEEK_END);
            len = ftell(fin) - startaddr*16 - headersize;
        }
        buffer = malloc(len);
        if (!buffer) {
            printf("failed to allocate %u bytes for entry %u\n", len, i);
            return 1;
        }
        fseek(fin, startaddr*16 + headersize, SEEK_SET);
        if (fread(buffer, sizeof(char), len, fin) != len) {
            printf("failed to read entry data\n");
            return 1;
        }
        if (argc == 3) {
            sprintf(outname, "%.3u.BIN", i);
        } else {
            sprintf(outname, "%s%.3u.BIN", inbasename, i);
        }
        fout = fopen(outname, "wb");
        if (!fout) {
            printf("failed to open %s for writing\n", outname);
            return 1;
        }
        fwrite(buffer, sizeof(char), len, fout);
        fclose(fout);
        free(buffer);
    }
    free(outname);
    fclose(fin);
    return 0;
}
