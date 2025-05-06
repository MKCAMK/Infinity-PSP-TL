#include <stdio.h>
#include <stdlib.h>
#include "lzss.h"
#include <assert.h>

int main(int argc, char *argv[]) {
    long in_size;
    unsigned out_size;
    char *in, *out;
    FILE *fin, *fout;
    size_t sret;

    if (argc != 3) {
        printf("usage: decompressbip in.bip out/\n");
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

    in = malloc(in_size);
    assert(in);
    sret = fread(in, 1, in_size, fin);
    assert(sret == (unsigned)in_size);
    fclose(fin);

    out_size = *(unsigned*)in;

    /* a workaround for 16-byte aligned BIP files */
    out = malloc(out_size+15);
    assert(out);

    decompress_lzss((unsigned char*)out, (unsigned char*)in+4, in_size-4);

    fwrite(out, 1, out_size, fout);

    free(in);
    free(out);
    fclose(fout);
    return 0;
}
