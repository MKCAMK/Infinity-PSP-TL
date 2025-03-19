#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    FILE *fout;
    unsigned count = 0, headersize = 0, divlen = 0, i;
    if (argc < 3) {
        printf("usage: repack_cnt <TARGET.CNT> <FILE1> [FILE2] [...]\n");
        return 1;
    }
    fout = fopen(argv[1], "wb");
    if (!fout) {
        printf("failed to open %s\n", argv[1]);
        return 1;
    }
    count = argc - 2;
    headersize = (4 + count*4 + 15) & ~15;
    /* printf("processing %u entries. header size %u\n", count, headersize); */
    fwrite(&count, sizeof(unsigned), 1, fout);
    for (i = 0; i < count; ++i) {
        FILE *fileentry;
        char *buffer;
        long filesize, j;
        fileentry = fopen(argv[i+2], "rb");
        if (!fileentry) {
            printf("failed to open %s\n", argv[i+2]);
            return 1;
        }
        fseek(fileentry, 0, SEEK_END);
        filesize = ftell(fileentry);
        rewind(fileentry);
        /* printf("writing len: %u. pos %ld\n", divlen*16, ftell(fout)); */
        fwrite(&divlen, sizeof(unsigned), 1, fout);
        fseek(fout, headersize + divlen*16, SEEK_SET);
        divlen += (filesize + 15) / 16;
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
        for (j = 0; j < (-filesize & 15); ++j) {
            fputc(0, fout);
        }
        fseek(fout, i*4+8, SEEK_SET);
    }
    fseek(fout, 4+count*4, SEEK_SET);
    for (i = 0; i < headersize - (4+count*4); ++i) {
        fputc(0, fout);
    }
    fclose(fout);
    printf("wrote %u bytes to %s\n", divlen*16, argv[1]);
    return 0;
}
