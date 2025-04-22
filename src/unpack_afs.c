#define _POSIX_C_SOURCE 1
#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

#if defined(__unix__) || defined(__unix) || (defined(__APPLE__) && defined(__MACH__))
#include <unistd.h>
#include <sys/stat.h>
#elif defined(_WIN32)
#include <direct.h>
#define mkdir(path, mode) _mkdir(path)
#define chdir _chdir
#else
#define NO_JADIR
#endif

#define AFS_MAGIC "AFS"

#pragma pack(push, 1)
struct sta {
    unsigned pos;
    unsigned len;
} /* __attribute__((packed)) */;
#pragma pack(pop)

#pragma pack(push, 1)
struct stb {
    char name[32];
    int unk1; /* filetype ? */
    int unk2;
    int unk3;
    unsigned len;
} /* __attribute__((packed)) */;
#pragma pack(pop)

int main(int argc, char *argv[]) {
    char magic[sizeof(AFS_MAGIC)];
    size_t sret;
    FILE *fin;
    unsigned i, entries;
    struct sta *stas;
    struct stb *stbs;

#ifndef NO_JADIR
    char *jadir;
    if (argc != 2 && argc != 3) {
        printf("usage: %s in.afs [ja/]\n", argv[0]);
        return 0;
    }
    jadir = (argc == 3) ? argv[2] : NULL;
#else
    if (argc != 2) {
        printf("usage: %s in.afs\n", argv[0]);
        return 0;
    }
#endif

    fin = fopen(argv[1], "rb");
    if (!fin) {
        printf("failed to open %s\n", argv[1]);
        return 1;
    }

    sret = fread(magic, 1, sizeof(AFS_MAGIC), fin);
    assert(sret == sizeof(AFS_MAGIC));
    if (memcmp(magic, AFS_MAGIC, sizeof(AFS_MAGIC)) != 0) {
        printf("not an AFS archive\n");
        return 1;
    }

    sret = fread(&entries, sizeof(unsigned), 1, fin);
    assert(sret == 1);

    stas = malloc((entries+1)*sizeof(struct sta));
    assert(stas);
    sret = fread(stas, sizeof(struct sta), entries+1, fin);
    assert(sret == entries+1);

    stbs = malloc(entries*sizeof(struct stb));
    assert(stbs);
    fseek(fin, stas[entries].pos, SEEK_SET);
    sret = fread(stbs, sizeof(struct stb), entries, fin);
    assert(sret == entries);

#ifndef NO_JADIR
    if (jadir) {
        (void)mkdir(jadir, 0755);
        if (chdir(jadir) == -1) {
            printf("failed to cd to %s\n", jadir);
            return 1;
        }
    }
#endif
    for (i = 0; i < entries; ++i) {
        char *buffer;
        FILE *fout;
        if (stas[i].pos == 0) {
            continue;
        }
        printf("-> %s\n", stbs[i].name);
        if (strpbrk(stbs[i].name, "/\\:")) {
            printf("unsafe filename\n");
            return 1;
        }
        fout = fopen(stbs[i].name, "wb");
        if (!fout) {
            printf("failed to create %s\n", stbs[i].name);
            return 1;
        }
        buffer = malloc(stas[i].len);
        assert(buffer);
        fseek(fin, stas[i].pos, SEEK_SET);
        sret = fread(buffer, 1, stas[i].len, fin);
        assert(sret == stas[i].len);
        sret = fwrite(buffer, 1, stas[i].len, fout);
        assert(sret == stas[i].len);
        free(buffer);
        fclose(fout);
    }

    fclose(fin);
    free(stas);
    free(stbs);
    return 0;
}
