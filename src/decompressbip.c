#include "my_mmap.h"
#include "lzss.h"

int main(int argc, char **argv) {
    assert2(argc==3, "usage: %s in.bip out\n", argv[0]);
    off_t in_size;
    uint8_t *in = mmap_file(argv[1], &in_size);
    int32_t out_size = *(int32_t*)in;

    uint8_t *out = malloc(out_size);
    int actual_size = decompress_lzss(out, in+4, in_size-4);

    write_file(argv[2], out, actual_size);
    free(out);
    return 0;
}
