#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    FILE *fout;
    unsigned i, count = 0, headersize = 0, len16 = 0;

    if (argc < 3) {
        printf("usage: pack_cnt <TARGET.CNT> <FILE1> [FILE2] [...]\n");
        return 1;
    }

    fout = fopen(argv[1], "wb");
    if (!fout) {
        printf("failed to open %s\n", argv[1]);
        return 1;
    }

    count = argc - 2;
    headersize = (4 + count*4 + 15) & ~15;

    fwrite(&count, sizeof(unsigned), 1, fout);
    for (i = 0; i < count; ++i) {
        FILE *fileentry;
        char *buffer;
        long filesize;

        fseek(fout, 4+i*4, SEEK_SET);

        fileentry = fopen(argv[i+2], "rb");
        if (!fileentry) {
            printf("failed to open %s\n", argv[i+2]);
            return 1;
        }

        fseek(fileentry, 0, SEEK_END);
        filesize = ftell(fileentry);
        rewind(fileentry);

        /* printf("writing len: %u. pos %ld\n", len16*16, ftell(fout)); */
        fwrite(&len16, sizeof(unsigned), 1, fout);
        fseek(fout, headersize + len16*16, SEEK_SET);
        len16 += (filesize + 15) / 16;

        buffer = malloc(filesize);
        if (!buffer) {
            printf("failed to allocate buffer of %ld bytes for %s\n", filesize, argv[i+2]);
            return 1;
        }
        if (fread(buffer, sizeof(char), filesize, fileentry) != (unsigned long)filesize) {
            printf("failed to read %s\n", argv[i+2]);
            return 1;
        }
        fclose(fileentry);
        fwrite(buffer, sizeof(char), filesize, fout);
        free(buffer);
    }
    fseek(fout, headersize+len16*16-1, SEEK_SET);
    fputc(0, fout);

    fclose(fout);
    printf("wrote %u entries (%u bytes) to %s\n", count, len16*16, argv[1]);
    return 0;
}
