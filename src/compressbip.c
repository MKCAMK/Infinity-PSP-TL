#include <stdio.h>
#include <stdlib.h>
#include "lzss.h"
#include <assert.h>

int main(int argc, char *argv[]) {
    long in_size;
    unsigned out_size, compressed_size;
    char *in, *out, *out_end;
    FILE *fin, *fout;
    size_t sret;

    if (argc != 3) {
        printf("usage: compressbip in out.bip\n");
        return 0;
    }

    fin = fopen(argv[1], "rb");
    if (!fin) {
        printf("failed to open %s\n", argv[1]);
        return 1;
    }
    fout = fopen(argv[2], "wb");
    if (!fout) {
        printf("failed to open %s\n", argv[2]);
        return 1;
    }
    fseek(fin, 0, SEEK_END);
    in_size = ftell(fin);
    assert(in_size != -1);
    rewind(fin);
    printf("Original size: %ld bytes\n", in_size);

    in = malloc(in_size);
    assert(in);
    sret = fread(in, 1, in_size, fin);
    assert(sret == (unsigned)in_size);
    fclose(fin);

    out_size = ((unsigned)in_size*9+7)/8 + 4; /* worst case */
    out = malloc(out_size);
    assert(out);

    out_end = (char*)compress_lzss((unsigned char*)out+4, out_size-4, (unsigned char*)in, in_size);
    compressed_size = out_end - out;
    printf("Compressed size: %u bytes\n", compressed_size);

    *(unsigned*)out = in_size;
    fwrite(out, 1, compressed_size, fout);

    free(in);
    free(out);
    fclose(fout);
    return 0;
}
