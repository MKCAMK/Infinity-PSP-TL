#define _POSIX_C_SOURCE 1
#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

#if defined(__unix__) || defined(__unix) || (defined(__APPLE__) && defined(__MACH__))
#include <libgen.h>
#include <unistd.h>
#elif defined(_WIN32)
#include <direct.h>
#define mkdir(path, mode) _mkdir(path)
#define chdir _chdir
#else
#define NO_OUTDIR
#endif

int main(int argc, char *argv[]) {
    FILE *fin;
    unsigned count = 0, headersize, i;

#ifndef NO_OUTDIR
    char* outdir;
    if (argc != 2 && argc != 3) {
        printf("usage: unpack_cnt <SOURCE.CNT> [OUT_DIR]\n");
        return 1;
    }
    outdir = (argc == 3) ? argv[2] : NULL;
#else
    if (argc != 2) {
        printf("usage: unpack_cnt <SOURCE.CNT>\n");
        return 1;
    }
#endif

    fin = fopen(argv[1], "rb");
    if (!fin) {
        printf("failed to open %s\n", argv[1]);
        return 1;
    }

#ifndef NO_OUTDIR
    if (outdir) {
        (void)mkdir(argv[2], 0755);
        if (chdir(argv[2]) == -1) {
            printf("chdir failed\n");
            return 1;
        }
    }
#endif

    if (fread(&count, sizeof(unsigned), 1, fin) != 1) {
        printf("failed to read file count\n");
        return 1;
    }
    headersize = (4 + count*4 + 15) & ~15;

    for (i = 0; i < count; ++i) {
        unsigned startaddr, len;
        char *buffer, outname[15];
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

        sprintf(outname, "%.3u.BIN", i);
        fout = fopen(outname, "wb");
        if (!fout) {
            printf("failed to open %s for writing\n", outname);
            return 1;
        }

        fwrite(buffer, sizeof(char), len, fout);
        fclose(fout);
        free(buffer);
    }

    fclose(fin);
    printf("extracted %u entries\n", count);
    return 0;
}
