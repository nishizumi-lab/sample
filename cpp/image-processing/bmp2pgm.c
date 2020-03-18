#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <math.h>
#include <string.h>

/* #define DEBUG */
#if defined(DEBUG)
#include "xmalloc.h"
#else
#define xmalloc(x, y) malloc(x)
#define xfree(x, y) free(x)
#define xrealloc(x, y, z) realloc(x, y)
#define xmallocdump()
#endif
/* for xmalloc.c */
#define IDRGB     1001
#define IDPALETTE 1002
#define IDBMP     1003

#define NBYTE  1
#define NWORD  2
#define NDWORD 4

int LittleEndianRead(unsigned long *data, int size, FILE *fp) {
  unsigned char lsb;
  unsigned long msb;
  if (size == 0) {
    *data = 0;
    return 1;
  }
  if (fread(&lsb, 1, 1, fp) != 1)
    return -1;
  if (LittleEndianRead(&msb, size - 1, fp) < 0)
    return -1;
  *data = (unsigned long)lsb | (msb << 8);
  return 1;
}

typedef struct {
  unsigned long bfType1;
  unsigned long bfType2;
  unsigned long bfSize;
  unsigned long bfReserved1;
  unsigned long bfReserved2;
  unsigned long bfOffBits;
} BitmapFileHeader;

int bmHeaderCheck(FILE *fp, BitmapFileHeader *bh) {
  assert(sizeof(unsigned long) >= 4);
  if (LittleEndianRead(&(bh->bfType1), NBYTE, fp) < 0)
    goto error_NotRead;
  if (LittleEndianRead(&(bh->bfType2), NBYTE, fp) < 0)
    goto error_NotRead;
  if (LittleEndianRead(&bh->bfSize, NDWORD, fp) < 0)
    goto error_NotRead;
  if (LittleEndianRead(&bh->bfReserved1, NWORD, fp) < 0)
    goto error_NotRead;
  if (LittleEndianRead(&bh->bfReserved2, NWORD, fp) < 0)
    goto error_NotRead;
  if (LittleEndianRead(&bh->bfOffBits, NDWORD, fp) < 0)
    goto error_NotRead;
#if 0
  printf("read:bfType1: %c\n", (char)bh->bfType1);
  printf("read:bfType2: %c\n", (char)bh->bfType2);
  printf("read:bfSize: %lu\n", bh->bfSize);
  printf("read:bfReserved1: %lu\n", bh->bfReserved1);
  printf("read:bfReserved2: %lu\n", bh->bfReserved2);
  printf("read:bfOffBits: %lu\n", bh->bfOffBits);
  putchar('\n');
#endif
  if (bh->bfType1 != 'B' || bh->bfType2 != 'M')
    goto error_NotBitmap;
  if (bh->bfReserved1 != 0 || bh->bfReserved2 != 0)
    goto error_NotBitmap;
  return 1;

error_NotBitmap:
  fprintf(stderr, "cannot find bmp header\n");
  return 0;
error_NotRead:
  fprintf(stderr, "cannot read bmp header\n");
  return 0;
}

typedef struct {
  unsigned long biSize;
  long biWidth;
  long biHeight;
  unsigned long biPlanes;
  unsigned long biBitCount;
  unsigned long biCompression;
  unsigned long biSizeImage;
  long biXPixPerMeter;
  long biYPixPerMeter;
  unsigned long biClrUsed;
  unsigned long biClrImportant;
} BitmapInfoHeader;

int bmInfoHeaderCheck(FILE *fp, BitmapInfoHeader *bi) {
  assert(sizeof(unsigned long) >= 4);
  assert(sizeof(long) >= 4);
  if (LittleEndianRead(&bi->biSize, NDWORD, fp) < 0)
    goto error_NotRead;
  if (bi->biSize == 12) {
    /* not supported */
  } else if (bi->biSize == 40) {
    if (LittleEndianRead((unsigned long *)&bi->biWidth, NDWORD, fp) < 0)
      goto error_NotRead;
    if (LittleEndianRead((unsigned long *)&bi->biHeight, NDWORD, fp) < 0)
      goto error_NotRead;
    if (LittleEndianRead(&bi->biPlanes, NWORD, fp) < 0)
      goto error_NotRead;
    if (LittleEndianRead(&bi->biBitCount, NWORD, fp) < 0)
      goto error_NotRead;
    if (LittleEndianRead(&bi->biCompression, NDWORD, fp) < 0)
      goto error_NotRead;
    if (LittleEndianRead(&bi->biSizeImage, NDWORD, fp) < 0)
      goto error_NotRead;
    if (LittleEndianRead((unsigned long *)&bi->biXPixPerMeter, NDWORD, fp) < 0)
      goto error_NotRead;
    if (LittleEndianRead((unsigned long *)&bi->biYPixPerMeter, NDWORD, fp) < 0)
      goto error_NotRead;
    if (LittleEndianRead(&bi->biClrUsed, NDWORD, fp) < 0)
      goto error_NotRead;
    if (LittleEndianRead(&bi->biClrImportant, NDWORD, fp) < 0)
      goto error_NotRead;
  } else {
    goto error_NotSupported1;
  }
#if 0
  printf("read:biSize: %lu\n", bi->biSize);
  printf("read:biWidth: %ld\n", bi->biWidth);
  printf("read:biHeight: %ld\n", bi->biHeight);
  printf("read:biPlanes: %lu\n", bi->biPlanes);
  printf("read:biBitcount: %lu\n", bi->biBitCount);
  if (bi->biSize == 40) {
    printf("read:biCompression: %lu\n", bi->biCompression);
    printf("read:biSizeImage: %lu\n", bi->biSizeImage);
    printf("read:biXPixPerMeter %ld\n", bi->biXPixPerMeter);
    printf("read:biYPixPerMeter %ld\n", bi->biYPixPerMeter);
    printf("read:biClrUsed: %lu\n", bi->biClrUsed);
    printf("read:biClrImporant: %lu\n", bi->biClrImportant);
  }
#endif
  if (bi->biSize != 40)
    goto error_NotSupported1;
  if (bi->biPlanes != 1)
    goto error_NotSupported2;
  if (bi->biBitCount != 24 && bi->biBitCount != 8 && bi->biBitCount != 4)
    goto error_NotSupported3;
  if (bi->biCompression != 0)
    goto error_NotSupported4;
  return 1;

error_NotSupported1:
  fprintf(stderr, "info header size: %lu, this format is not supported\n", bi->biSize);
  return 0;
error_NotSupported2:
  fprintf(stderr, "biPlanes: %lu, this format is not supported\n", bi->biPlanes);
  return 0;
error_NotSupported3:
  fprintf(stderr, "biBitCount: %lu, this format is not supported\n", bi->biBitCount);
  return 0;
error_NotSupported4:
  fprintf(stderr, "biCompression: %lu, this format is not supported\n", bi->biCompression);
  return 0;
error_NotRead:
#if 0
  printf("read:biSize: %lu\n", bi->biSize);
  printf("read:biWidth: %ld\n", bi->biWidth);
  printf("read:biHeight: %ld\n", bi->biHeight);
  printf("read:biPlanes: %lu\n", bi->biPlanes);
  printf("read:biBitcount: %lu\n", bi->biBitCount);
  if (bi->biSize == 40) {
    printf("read:biCompression: %lu\n", bi->biCompression);
    printf("read:biSizeImage: %lu\n", bi->biSizeImage);
    printf("read:biXPixPerMeter %ld\n", bi->biXPixPerMeter);
    printf("read:biYPixPerMeter %ld\n", bi->biYPixPerMeter);
    printf("read:biClrUsed: %lu\n", bi->biClrUsed);
    printf("read:biClrImporant: %lu\n", bi->biClrImportant);
  }
#endif
  fprintf(stderr, "cannot read bmp info header\n");
  return 0;
}

int isFtellGood(FILE *fp, unsigned long pos) {
  return (unsigned long)ftell(fp) == pos;
}

long iabs(long n) {
  return (n > 0) ? n : -n;
}


void task_read24(FILE *fp, BitmapFileHeader *bheader, BitmapInfoHeader *binfo,
               unsigned char **dataR, unsigned char **dataG,
               unsigned char **dataB)
{
  long x, y, n;
  unsigned char dummy;
  int c;
  if (!isFtellGood(fp, bheader->bfOffBits)) {
    fprintf(stderr, "Header or Image Data is corrupted.\n");
    return;
  }
  *dataR = xmalloc(sizeof(char) * iabs(binfo->biWidth) * iabs(binfo->biHeight), IDRGB);
  *dataG = xmalloc(sizeof(char) * iabs(binfo->biWidth) * iabs(binfo->biHeight), IDRGB);
  *dataB = xmalloc(sizeof(char) * iabs(binfo->biWidth) * iabs(binfo->biHeight), IDRGB);  
  if (*dataR == NULL || *dataG == NULL || *dataB == NULL) {
    fprintf(stderr, "cannot alloc. enough memory.\n");
    return;
  }
  for (y = 0; y < iabs(binfo->biHeight); y++) {
    c = 0;
    for (x = 0; x < iabs(binfo->biWidth); x++) {
      fread((*dataB + y * iabs(binfo->biWidth) + x), 1, 1, fp);
      fread((*dataG + y * iabs(binfo->biWidth) + x), 1, 1, fp);
      fread((*dataR + y * iabs(binfo->biWidth) + x), 1, 1, fp);
      c += 3;
    }
    while (c % 4 != 0) {
      fread(&dummy, 1, 1, fp);
      c++;
    }
  }
  n = iabs(binfo->biWidth) * 3;
  if (n % 4 > 0)
    n += 4 - (n % 4);
  binfo->biSizeImage = n * iabs(binfo->biHeight);
  bheader->bfSize = binfo->biSizeImage + binfo->biSize + 14;
}

void task_read_palette(FILE *fp, BitmapFileHeader *bh, BitmapInfoHeader *bi,
                       unsigned char **dataPalette)
{
  int i, max;
  unsigned char dummy;
  if ((max = bi->biClrUsed) == 0) {
    switch (bi->biBitCount) {
    case 4:
      max = 16;
      break;
    case 8:
      max = 256;
      break;
    }
  }
  *dataPalette = xmalloc(sizeof(char) * 3 * max, IDPALETTE);
  if (*dataPalette == NULL) {
    fprintf(stderr, "cannot alloc. enough memory.\n");
    return;
  }
  for (i = 0; i < max; i++) {
    fread((*dataPalette + 3 * i + 0), 1, 1, fp);
    fread((*dataPalette + 3 * i + 1), 1, 1, fp);
    fread((*dataPalette + 3 * i + 2), 1, 1, fp);
    fread(&dummy, 1, 1, fp);    
  }
}

void task_read8(FILE *fp, BitmapFileHeader *bheader, BitmapInfoHeader *binfo,
               unsigned char **dataR, unsigned char **dataG,
               unsigned char **dataB, unsigned char *dataPalette)
{
  long x, y, n;
  unsigned char data;
  int c;

  if (!isFtellGood(fp, bheader->bfOffBits)) {
    fprintf(stderr, "Header or Image Data is corrupted.\n");
    return;
  }
  *dataR = xmalloc(sizeof(char) * iabs(binfo->biWidth) * iabs(binfo->biHeight), IDRGB);
  *dataG = xmalloc(sizeof(char) * iabs(binfo->biWidth) * iabs(binfo->biHeight), IDRGB);
  *dataB = xmalloc(sizeof(char) * iabs(binfo->biWidth) * iabs(binfo->biHeight), IDRGB);  
  if (*dataR == NULL || *dataG == NULL || *dataB == NULL) {
    fprintf(stderr, "cannot alloc. enough memory.\n");
    return;
  }
  for (y = 0; y < iabs(binfo->biHeight); y++) {
    c = 0;
    for (x = 0; x < iabs(binfo->biWidth); x++) {
      fread(&data, 1, 1, fp);
      *(*dataB + y * iabs(binfo->biWidth) + x) = dataPalette[3 * data + 0];
      *(*dataG + y * iabs(binfo->biWidth) + x) = dataPalette[3 * data + 1];
      *(*dataR + y * iabs(binfo->biWidth) + x) = dataPalette[3 * data + 2];
      c++;
    }
    while (c % 4 != 0) {
      fread(&data, 1, 1, fp);
      c++;
    }
  }
  n = iabs(binfo->biWidth) * 3;
  if (n % 4 > 0)
    n += 4 - (n % 4);
  binfo->biSizeImage = n * iabs(binfo->biHeight);
  bheader->bfSize = binfo->biSizeImage + binfo->biSize + 14;
  bheader->bfOffBits = 54;
  binfo->biBitCount = 24;
  binfo->biClrUsed = 0;
  binfo->biClrImportant = 0;
}

void task_read4(FILE *fp, BitmapFileHeader *bheader, BitmapInfoHeader *binfo,
               unsigned char **dataR, unsigned char **dataG,
               unsigned char **dataB, unsigned char *dataPalette)
{
  long x, y, n;
  unsigned char data, rdata;
  int c;
  int bitHighLow;

  if (!isFtellGood(fp, bheader->bfOffBits)) {
    fprintf(stderr, "Header or Image Data is corrupted.\n");
    return;
  }
  *dataR = xmalloc(sizeof(char) * iabs(binfo->biWidth) * iabs(binfo->biHeight), IDRGB);
  *dataG = xmalloc(sizeof(char) * iabs(binfo->biWidth) * iabs(binfo->biHeight), IDRGB);
  *dataB = xmalloc(sizeof(char) * iabs(binfo->biWidth) * iabs(binfo->biHeight), IDRGB);  
  if (*dataR == NULL || *dataG == NULL || *dataB == NULL) {
    fprintf(stderr, "cannot alloc. enough memory.\n");
    return;
  }
  bitHighLow = 1;
  for (y = 0; y < iabs(binfo->biHeight); y++) {
    c = 0;
    for (x = 0; x < iabs(binfo->biWidth); x++) {
      if (bitHighLow) {
        fread(&rdata, 1, 1, fp);
        data = rdata & 0xf0;
        data >>= 4;
        bitHighLow = 0;
      } else {
        data = rdata & 0x0f;
        bitHighLow = 1;
      }
      *(*dataB + y * iabs(binfo->biWidth) + x) = dataPalette[3 * data + 0];
      *(*dataG + y * iabs(binfo->biWidth) + x) = dataPalette[3 * data + 1];
      *(*dataR + y * iabs(binfo->biWidth) + x) = dataPalette[3 * data + 2];
      c++;
    }
    while (c % 4 != 0) {
      fread(&data, 1, 1, fp);
      c++;
    }
  }
  n = iabs(binfo->biWidth) * 3;
  if (n % 4 > 0)
    n += 4 - (n % 4);
  binfo->biSizeImage = n * iabs(binfo->biHeight);
  bheader->bfSize = binfo->biSizeImage + binfo->biSize + 14;
  bheader->bfOffBits = 54;
  binfo->biBitCount = 24;
  binfo->biClrUsed = 0;
  binfo->biClrImportant = 0;
}

void LittleEndianWrite(unsigned long *data, int size, FILE *fp) {
  unsigned char lsb;
  unsigned long msb;
  if (size == 0)
    return;
  lsb = (unsigned char)(*data & 0xff);
  fwrite(&lsb, 1, 1, fp);
  msb = *data >> 8;
  LittleEndianWrite(&msb, size - 1, fp);
}

void task_write_header(FILE *fp, BitmapFileHeader *bh) {
  assert(sizeof(unsigned long) >= 4);
  assert(sizeof(long) >= 4);
  LittleEndianWrite(&(bh->bfType1), NBYTE, fp);
  LittleEndianWrite(&(bh->bfType2), NBYTE, fp);
  LittleEndianWrite(&(bh->bfSize), NDWORD, fp);
  LittleEndianWrite(&(bh->bfReserved1), NWORD, fp);
  LittleEndianWrite(&(bh->bfReserved2), NWORD, fp);
  LittleEndianWrite(&(bh->bfOffBits), NDWORD, fp);
#if 0
  printf("write:bfType1: %c\n", (char)bh->bfType1);
  printf("write:bfType2: %c\n", (char)bh->bfType2);
  printf("write:bfSize: %lu\n", bh->bfSize);
  printf("write:bfReserved1: %lu\n", bh->bfReserved1);
  printf("write:bfReserved2: %lu\n", bh->bfReserved2);
  printf("write:bfOffBits: %lu\n", bh->bfOffBits);
#endif
}

void task_write_info(FILE *fp, BitmapInfoHeader *bi) {
  assert(sizeof(unsigned short) == 2);
  assert(sizeof(unsigned long) == 4);
  assert(sizeof(long) == 4);
  LittleEndianWrite(&(bi->biSize), NDWORD, fp);
  LittleEndianWrite((unsigned long *)&(bi->biWidth), NDWORD, fp);
  LittleEndianWrite((unsigned long *)&(bi->biHeight), NDWORD, fp);
  LittleEndianWrite(&(bi->biPlanes), NWORD, fp);
  LittleEndianWrite(&(bi->biBitCount), NWORD, fp);
  LittleEndianWrite(&(bi->biCompression), NDWORD, fp);
  LittleEndianWrite(&(bi->biSizeImage), NDWORD, fp);
  LittleEndianWrite((unsigned long *)&(bi->biXPixPerMeter), NDWORD, fp);
  LittleEndianWrite((unsigned long *)&(bi->biYPixPerMeter), NDWORD, fp);
  LittleEndianWrite(&(bi->biClrUsed), NDWORD, fp);
  LittleEndianWrite(&(bi->biClrImportant), NDWORD, fp);
#if 0
  printf("write:biSize: %lu\n", bi->biSize);
  printf("write:biWidth: %ld\n", bi->biWidth);
  printf("write:biHeight: %ld\n", bi->biHeight);
  printf("write:biPlanes: %lu\n", bi->biPlanes);
  printf("write:biBitcount: %lu\n", bi->biBitCount);
  printf("write:biCompression: %lu\n", bi->biCompression);
  printf("write:biSizeImage: %lu\n", bi->biSizeImage);
  printf("write:biXPixPerMeter %ld\n", bi->biXPixPerMeter);
  printf("write:biYPixPerMeter %ld\n", bi->biYPixPerMeter);
  printf("write:biClrUsed: %lu\n", bi->biClrUsed);
  printf("write:biClrImporant: %lu\n", bi->biClrImportant);
#endif
}

void task_write24(FILE *fp,
                  BitmapFileHeader *bh, BitmapInfoHeader *bi,
                  unsigned char *dataR,
                  unsigned char *dataG,
                  unsigned char *dataB) {
  int x, y;
  int c;
  unsigned char dummy = '\0';
  task_write_header(fp, bh);
  task_write_info(fp, bi);
  for (y = 0; y < iabs(bi->biHeight); y++) {
    c = 0;
    for (x = 0; x < iabs(bi->biWidth); x++) {
      fwrite(&dataB[y * iabs(bi->biWidth) + x], 1, 1, fp);
      fwrite(&dataG[y * iabs(bi->biWidth) + x], 1, 1, fp);
      fwrite(&dataR[y * iabs(bi->biWidth) + x], 1, 1, fp);
      c += 3;
    }
    while (c % 4 != 0) {
      fwrite(&dummy, 1, 1, fp);
      c++;
    }
  }
}

/* ------------------------------------------------------------------------- */
struct BMP24 {
  BitmapFileHeader bh;
  BitmapInfoHeader bi;
  unsigned char *dataR;
  unsigned char *dataG;
  unsigned char *dataB;
  unsigned char *dataPalette;
};

int BMP24_read(FILE *fp, struct BMP24 *bmp) {
  if (!bmHeaderCheck(fp, &(bmp->bh)))
    return 0;
  if (!bmInfoHeaderCheck(fp, &(bmp->bi)))
    return 0;
  bmp->dataR = bmp->dataG = bmp->dataB = bmp->dataPalette = NULL;
  if ((bmp->bi).biBitCount == 24) {
    task_read24(fp, &(bmp->bh), &(bmp->bi),
                &(bmp->dataR), &(bmp->dataG), &(bmp->dataB));
  } else if ((bmp->bi).biBitCount == 8) {
    task_read_palette(fp, &bmp->bh, &bmp->bi, &bmp->dataPalette);
    task_read8(fp, &bmp->bh, &bmp->bi,
               &bmp->dataR, &bmp->dataG, &bmp->dataB, bmp->dataPalette);
    xfree(bmp->dataPalette, IDPALETTE);
    bmp->dataPalette = NULL;
  } else if ((bmp->bi).biBitCount == 4) {
    task_read_palette(fp, &bmp->bh, &bmp->bi, &bmp->dataPalette);
    task_read4(fp, &bmp->bh, &bmp->bi,
               &bmp->dataR, &bmp->dataG, &bmp->dataB, bmp->dataPalette);
    xfree(bmp->dataPalette, IDPALETTE);
    bmp->dataPalette = NULL;
  }
  if (!(bmp->dataR && bmp->dataG && bmp->dataB)) {
    xfree(bmp->dataR, IDRGB);
    xfree(bmp->dataG, IDRGB);
    xfree(bmp->dataB, IDRGB);
    return 0;
  }
  return 1;
}

void BMP24_write(FILE *fp, struct BMP24 *bmp) {
  task_write24(fp, &bmp->bh, &bmp->bi,
               bmp->dataR, bmp->dataG, bmp->dataB);
}

void BMP24_release(struct BMP24 *bmp) {
  if (bmp->dataR) xfree(bmp->dataR, IDRGB);
  if (bmp->dataG) xfree(bmp->dataG, IDRGB);
  if (bmp->dataB) xfree(bmp->dataB, IDRGB);
  if (bmp->dataPalette) xfree(bmp->dataPalette, IDPALETTE);
}

/* ------------------------------------------------------------------------- */
void task_colorbmp2gray(struct BMP24 *bmp) {
  unsigned int c;
  long w, h, x, y;
  w = iabs((bmp->bi).biWidth);
  h = iabs((bmp->bi).biHeight);
  for (y = 0; y < h; y++) {
    for (x = 0; x < w; x++) {
      c = bmp->dataR[y * w + x] + bmp->dataG[y * w + x] + bmp->dataB[y * w + x];
      bmp->dataR[y * w + x] = bmp->dataG[y * w + x] = bmp->dataB[y * w + x] = (unsigned char)(c / 3);
    }
  }
}

/* ------------------------------------------------------------------------- */
void task_bmp2pgm(FILE *fpbmp, FILE *fppgm) {
  struct BMP24 *bmp;
  long Width, Height, y, x;

  bmp = xmalloc(sizeof(struct BMP24), IDBMP);
  if (!BMP24_read(fpbmp, bmp)) {
    fprintf(stderr, "not a bitmap file, aborted.\n");
    xfree(bmp, IDBMP);
    return;      
  }
  Width = iabs((bmp->bi).biWidth);
  Height = iabs((bmp->bi).biHeight);
  task_colorbmp2gray(bmp);
  fprintf(fppgm, "P2\n");
  fprintf(fppgm, "%ld %ld\n", Width, Height);
  fprintf(fppgm, "255\n");
  if ((bmp->bi).biHeight < 0) {
    for (y = 0; y < Height; y++) {
      for (x = 0; x < Width; x++)
        fprintf(fppgm, "%3d ", bmp->dataR[y * Width + x]);
      fprintf(fppgm, "\n");
    }
  } else {
    for (y = Height - 1; y >= 0; y--) {
      for (x = 0; x < Width; x++)
        fprintf(fppgm, "%3d ", bmp->dataR[y * Width + x]);
      fprintf(fppgm, "\n");
    }
  }
  BMP24_release(bmp);
  xfree(bmp, IDBMP);
}

int main(int argc, char **argv) {
  FILE *fpbmp, *fppgm;
  if (argc != 3) {
    fprintf(stderr, "usage: %s <filename:bmp> <filename:pgm>\n", argv[0]);
    exit(-1);
  }
  if ((fpbmp = fopen(argv[1], "r")) == 0) {
    fprintf(stderr, "cannot open the .bmp file for reading\n");
    exit(-1);
  }
  if ((fppgm = fopen(argv[2], "w")) == 0) {
    fprintf(stderr, "cannot open the .bgm file for writing\n");
    fclose(fpbmp);
    exit(-1);
  }
  task_bmp2pgm(fpbmp, fppgm);
  fclose(fpbmp);
  fclose(fppgm);
  xmallocdump();
  return 0;
}
/* end */