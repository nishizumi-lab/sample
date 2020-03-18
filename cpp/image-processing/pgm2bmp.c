#include stdio.h
#include stdlib.h
#include assert.h
#include math.h
#include string.h

 #define DEBUG 
#if defined(DEBUG)
#include xmalloc.h
#else
#define xmalloc(x, y) malloc(x)
#define xfree(x, y) free(x)
#define xrealloc(x, y, z) realloc(x, y)
#define xmallocdump()
#endif
 for xmalloc.c 
#define IDRGB     1001
#define IDPALETTE 1002
#define IDBMP     1003
#define ID_GETLINE 1004

#define NBYTE  1
#define NWORD  2
#define NDWORD 4

int LittleEndianRead(unsigned long data, int size, FILE fp) {
  unsigned char lsb;
  unsigned long msb;
  if (size == 0) {
    data = 0;
    return 1;
  }
  if (fread(&lsb, 1, 1, fp) != 1)
    return -1;
  if (LittleEndianRead(&msb, size - 1, fp)  0)
    return -1;
  data = (unsigned long)lsb  (msb  8);
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

int bmHeaderCheck(FILE fp, BitmapFileHeader bh) {
  assert(sizeof(unsigned long) = 4);
  if (LittleEndianRead(&(bh-bfType1), NBYTE, fp)  0)
    goto error_NotRead;
  if (LittleEndianRead(&(bh-bfType2), NBYTE, fp)  0)
    goto error_NotRead;
  if (LittleEndianRead(&bh-bfSize, NDWORD, fp)  0)
    goto error_NotRead;
  if (LittleEndianRead(&bh-bfReserved1, NWORD, fp)  0)
    goto error_NotRead;
  if (LittleEndianRead(&bh-bfReserved2, NWORD, fp)  0)
    goto error_NotRead;
  if (LittleEndianRead(&bh-bfOffBits, NDWORD, fp)  0)
    goto error_NotRead;
#if 0
  printf(readbfType1 %cn, (char)bh-bfType1);
  printf(readbfType2 %cn, (char)bh-bfType2);
  printf(readbfSize %lun, bh-bfSize);
  printf(readbfReserved1 %lun, bh-bfReserved1);
  printf(readbfReserved2 %lun, bh-bfReserved2);
  printf(readbfOffBits %lun, bh-bfOffBits);
  putchar('n');
#endif
  if (bh-bfType1 != 'B'  bh-bfType2 != 'M')
    goto error_NotBitmap;
  if (bh-bfReserved1 != 0  bh-bfReserved2 != 0)
    goto error_NotBitmap;
  return 1;

error_NotBitmap
  fprintf(stderr, cannot find bmp headern);
  return 0;
error_NotRead
  fprintf(stderr, cannot read bmp headern);
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

int bmInfoHeaderCheck(FILE fp, BitmapInfoHeader bi) {
  assert(sizeof(unsigned long) = 4);
  assert(sizeof(long) = 4);
  if (LittleEndianRead(&bi-biSize, NDWORD, fp)  0)
    goto error_NotRead;
  if (bi-biSize == 12) {
     not supported 
  } else if (bi-biSize == 40) {
    if (LittleEndianRead((unsigned long )&bi-biWidth, NDWORD, fp)  0)
      goto error_NotRead;
    if (LittleEndianRead((unsigned long )&bi-biHeight, NDWORD, fp)  0)
      goto error_NotRead;
    if (LittleEndianRead(&bi-biPlanes, NWORD, fp)  0)
      goto error_NotRead;
    if (LittleEndianRead(&bi-biBitCount, NWORD, fp)  0)
      goto error_NotRead;
    if (LittleEndianRead(&bi-biCompression, NDWORD, fp)  0)
      goto error_NotRead;
    if (LittleEndianRead(&bi-biSizeImage, NDWORD, fp)  0)
      goto error_NotRead;
    if (LittleEndianRead((unsigned long )&bi-biXPixPerMeter, NDWORD, fp)  0)
      goto error_NotRead;
    if (LittleEndianRead((unsigned long )&bi-biYPixPerMeter, NDWORD, fp)  0)
      goto error_NotRead;
    if (LittleEndianRead(&bi-biClrUsed, NDWORD, fp)  0)
      goto error_NotRead;
    if (LittleEndianRead(&bi-biClrImportant, NDWORD, fp)  0)
      goto error_NotRead;
  } else {
    goto error_NotSupported1;
  }
#if 0
  printf(readbiSize %lun, bi-biSize);
  printf(readbiWidth %ldn, bi-biWidth);
  printf(readbiHeight %ldn, bi-biHeight);
  printf(readbiPlanes %lun, bi-biPlanes);
  printf(readbiBitcount %lun, bi-biBitCount);
  if (bi-biSize == 40) {
    printf(readbiCompression %lun, bi-biCompression);
    printf(readbiSizeImage %lun, bi-biSizeImage);
    printf(readbiXPixPerMeter %ldn, bi-biXPixPerMeter);
    printf(readbiYPixPerMeter %ldn, bi-biYPixPerMeter);
    printf(readbiClrUsed %lun, bi-biClrUsed);
    printf(readbiClrImporant %lun, bi-biClrImportant);
  }
#endif
  if (bi-biSize != 40)
    goto error_NotSupported1;
  if (bi-biPlanes != 1)
    goto error_NotSupported2;
  if (bi-biBitCount != 24 && bi-biBitCount != 8 && bi-biBitCount != 4)
    goto error_NotSupported3;
  if (bi-biCompression != 0)
    goto error_NotSupported4;
  return 1;

error_NotSupported1
  fprintf(stderr, info header size %lu, this format is not supportedn, bi-biSize);
  return 0;
error_NotSupported2
  fprintf(stderr, biPlanes %lu, this format is not supportedn, bi-biPlanes);
  return 0;
error_NotSupported3
  fprintf(stderr, biBitCount %lu, this format is not supportedn, bi-biBitCount);
  return 0;
error_NotSupported4
  fprintf(stderr, biCompression %lu, this format is not supportedn, bi-biCompression);
  return 0;
error_NotRead
#if 0
  printf(readbiSize %lun, bi-biSize);
  printf(readbiWidth %ldn, bi-biWidth);
  printf(readbiHeight %ldn, bi-biHeight);
  printf(readbiPlanes %lun, bi-biPlanes);
  printf(readbiBitcount %lun, bi-biBitCount);
  if (bi-biSize == 40) {
    printf(readbiCompression %lun, bi-biCompression);
    printf(readbiSizeImage %lun, bi-biSizeImage);
    printf(readbiXPixPerMeter %ldn, bi-biXPixPerMeter);
    printf(readbiYPixPerMeter %ldn, bi-biYPixPerMeter);
    printf(readbiClrUsed %lun, bi-biClrUsed);
    printf(readbiClrImporant %lun, bi-biClrImportant);
  }
#endif
  fprintf(stderr, cannot read bmp info headern);
  return 0;
}

int isFtellGood(FILE fp, unsigned long pos) {
  return (unsigned long)ftell(fp) == pos;
}

long iabs(long n) {
  return (n  0)  n  -n;
}


void task_read24(FILE fp, BitmapFileHeader bheader, BitmapInfoHeader binfo,
               unsigned char dataR, unsigned char dataG,
               unsigned char dataB)
{
  long x, y, n;
  unsigned char dummy;
  int c;
  if (!isFtellGood(fp, bheader-bfOffBits)) {
    fprintf(stderr, Header or Image Data is corrupted.n);
    return;
  }
  dataR = xmalloc(sizeof(char)  iabs(binfo-biWidth)  iabs(binfo-biHeight), IDRGB);
  dataG = xmalloc(sizeof(char)  iabs(binfo-biWidth)  iabs(binfo-biHeight), IDRGB);
  dataB = xmalloc(sizeof(char)  iabs(binfo-biWidth)  iabs(binfo-biHeight), IDRGB);  
  if (dataR == NULL  dataG == NULL  dataB == NULL) {
    fprintf(stderr, cannot alloc. enough memory.n);
    return;
  }
  for (y = 0; y  iabs(binfo-biHeight); y++) {
    c = 0;
    for (x = 0; x  iabs(binfo-biWidth); x++) {
      fread((dataB + y  iabs(binfo-biWidth) + x), 1, 1, fp);
      fread((dataG + y  iabs(binfo-biWidth) + x), 1, 1, fp);
      fread((dataR + y  iabs(binfo-biWidth) + x), 1, 1, fp);
      c += 3;
    }
    while (c % 4 != 0) {
      fread(&dummy, 1, 1, fp);
      c++;
    }
  }
  n = iabs(binfo-biWidth)  3;
  if (n % 4  0)
    n += 4 - (n % 4);
  binfo-biSizeImage = n  iabs(binfo-biHeight);
  bheader-bfSize = binfo-biSizeImage + binfo-biSize + 14;
}

void task_read_palette(FILE fp, BitmapFileHeader bh, BitmapInfoHeader bi,
                       unsigned char dataPalette)
{
  int i, max;
  unsigned char dummy;
  if ((max = bi-biClrUsed) == 0) {
    switch (bi-biBitCount) {
    case 4
      max = 16;
      break;
    case 8
      max = 256;
      break;
    }
  }
  dataPalette = xmalloc(sizeof(char)  3  max, IDPALETTE);
  if (dataPalette == NULL) {
    fprintf(stderr, cannot alloc. enough memory.n);
    return;
  }
  for (i = 0; i  max; i++) {
    fread((dataPalette + 3  i + 0), 1, 1, fp);
    fread((dataPalette + 3  i + 1), 1, 1, fp);
    fread((dataPalette + 3  i + 2), 1, 1, fp);
    fread(&dummy, 1, 1, fp);    
  }
}

void task_read8(FILE fp, BitmapFileHeader bheader, BitmapInfoHeader binfo,
               unsigned char dataR, unsigned char dataG,
               unsigned char dataB, unsigned char dataPalette)
{
  long x, y, n;
  unsigned char data;
  int c;

  if (!isFtellGood(fp, bheader-bfOffBits)) {
    fprintf(stderr, Header or Image Data is corrupted.n);
    return;
  }
  dataR = xmalloc(sizeof(char)  iabs(binfo-biWidth)  iabs(binfo-biHeight), IDRGB);
  dataG = xmalloc(sizeof(char)  iabs(binfo-biWidth)  iabs(binfo-biHeight), IDRGB);
  dataB = xmalloc(sizeof(char)  iabs(binfo-biWidth)  iabs(binfo-biHeight), IDRGB);  
  if (dataR == NULL  dataG == NULL  dataB == NULL) {
    fprintf(stderr, cannot alloc. enough memory.n);
    return;
  }
  for (y = 0; y  iabs(binfo-biHeight); y++) {
    c = 0;
    for (x = 0; x  iabs(binfo-biWidth); x++) {
      fread(&data, 1, 1, fp);
      (dataB + y  iabs(binfo-biWidth) + x) = dataPalette[3  data + 0];
      (dataG + y  iabs(binfo-biWidth) + x) = dataPalette[3  data + 1];
      (dataR + y  iabs(binfo-biWidth) + x) = dataPalette[3  data + 2];
      c++;
    }
    while (c % 4 != 0) {
      fread(&data, 1, 1, fp);
      c++;
    }
  }
  n = iabs(binfo-biWidth)  3;
  if (n % 4  0)
    n += 4 - (n % 4);
  binfo-biSizeImage = n  iabs(binfo-biHeight);
  bheader-bfSize = binfo-biSizeImage + binfo-biSize + 14;
  bheader-bfOffBits = 54;
  binfo-biBitCount = 24;
  binfo-biClrUsed = 0;
  binfo-biClrImportant = 0;
}

void task_read4(FILE fp, BitmapFileHeader bheader, BitmapInfoHeader binfo,
               unsigned char dataR, unsigned char dataG,
               unsigned char dataB, unsigned char dataPalette)
{
  long x, y, n;
  unsigned char data, rdata;
  int c;
  int bitHighLow;

  if (!isFtellGood(fp, bheader-bfOffBits)) {
    fprintf(stderr, Header or Image Data is corrupted.n);
    return;
  }
  dataR = xmalloc(sizeof(char)  iabs(binfo-biWidth)  iabs(binfo-biHeight), IDRGB);
  dataG = xmalloc(sizeof(char)  iabs(binfo-biWidth)  iabs(binfo-biHeight), IDRGB);
  dataB = xmalloc(sizeof(char)  iabs(binfo-biWidth)  iabs(binfo-biHeight), IDRGB);  
  if (dataR == NULL  dataG == NULL  dataB == NULL) {
    fprintf(stderr, cannot alloc. enough memory.n);
    return;
  }
  bitHighLow = 1;
  for (y = 0; y  iabs(binfo-biHeight); y++) {
    c = 0;
    for (x = 0; x  iabs(binfo-biWidth); x++) {
      if (bitHighLow) {
        fread(&rdata, 1, 1, fp);
        data = rdata & 0xf0;
        data = 4;
        bitHighLow = 0;
      } else {
        data = rdata & 0x0f;
        bitHighLow = 1;
      }
      (dataB + y  iabs(binfo-biWidth) + x) = dataPalette[3  data + 0];
      (dataG + y  iabs(binfo-biWidth) + x) = dataPalette[3  data + 1];
      (dataR + y  iabs(binfo-biWidth) + x) = dataPalette[3  data + 2];
      c++;
    }
    while (c % 4 != 0) {
      fread(&data, 1, 1, fp);
      c++;
    }
  }
  n = iabs(binfo-biWidth)  3;
  if (n % 4  0)
    n += 4 - (n % 4);
  binfo-biSizeImage = n  iabs(binfo-biHeight);
  bheader-bfSize = binfo-biSizeImage + binfo-biSize + 14;
  bheader-bfOffBits = 54;
  binfo-biBitCount = 24;
  binfo-biClrUsed = 0;
  binfo-biClrImportant = 0;
}

void LittleEndianWrite(unsigned long data, int size, FILE fp) {
  unsigned char lsb;
  unsigned long msb;
  if (size == 0)
    return;
  lsb = (unsigned char)(data & 0xff);
  fwrite(&lsb, 1, 1, fp);
  msb = data  8;
  LittleEndianWrite(&msb, size - 1, fp);
}

void task_write_header(FILE fp, BitmapFileHeader bh) {
  assert(sizeof(unsigned long) = 4);
  assert(sizeof(long) = 4);
  LittleEndianWrite(&(bh-bfType1), NBYTE, fp);
  LittleEndianWrite(&(bh-bfType2), NBYTE, fp);
  LittleEndianWrite(&(bh-bfSize), NDWORD, fp);
  LittleEndianWrite(&(bh-bfReserved1), NWORD, fp);
  LittleEndianWrite(&(bh-bfReserved2), NWORD, fp);
  LittleEndianWrite(&(bh-bfOffBits), NDWORD, fp);
#if 0
  printf(writebfType1 %cn, (char)bh-bfType1);
  printf(writebfType2 %cn, (char)bh-bfType2);
  printf(writebfSize %lun, bh-bfSize);
  printf(writebfReserved1 %lun, bh-bfReserved1);
  printf(writebfReserved2 %lun, bh-bfReserved2);
  printf(writebfOffBits %lun, bh-bfOffBits);
#endif
}

void task_write_info(FILE fp, BitmapInfoHeader bi) {
  assert(sizeof(unsigned short) == 2);
  assert(sizeof(unsigned long) == 4);
  assert(sizeof(long) == 4);
  LittleEndianWrite(&(bi-biSize), NDWORD, fp);
  LittleEndianWrite((unsigned long )&(bi-biWidth), NDWORD, fp);
  LittleEndianWrite((unsigned long )&(bi-biHeight), NDWORD, fp);
  LittleEndianWrite(&(bi-biPlanes), NWORD, fp);
  LittleEndianWrite(&(bi-biBitCount), NWORD, fp);
  LittleEndianWrite(&(bi-biCompression), NDWORD, fp);
  LittleEndianWrite(&(bi-biSizeImage), NDWORD, fp);
  LittleEndianWrite((unsigned long )&(bi-biXPixPerMeter), NDWORD, fp);
  LittleEndianWrite((unsigned long )&(bi-biYPixPerMeter), NDWORD, fp);
  LittleEndianWrite(&(bi-biClrUsed), NDWORD, fp);
  LittleEndianWrite(&(bi-biClrImportant), NDWORD, fp);
#if 0
  printf(writebiSize %lun, bi-biSize);
  printf(writebiWidth %ldn, bi-biWidth);
  printf(writebiHeight %ldn, bi-biHeight);
  printf(writebiPlanes %lun, bi-biPlanes);
  printf(writebiBitcount %lun, bi-biBitCount);
  printf(writebiCompression %lun, bi-biCompression);
  printf(writebiSizeImage %lun, bi-biSizeImage);
  printf(writebiXPixPerMeter %ldn, bi-biXPixPerMeter);
  printf(writebiYPixPerMeter %ldn, bi-biYPixPerMeter);
  printf(writebiClrUsed %lun, bi-biClrUsed);
  printf(writebiClrImporant %lun, bi-biClrImportant);
#endif
}

void task_write24(FILE fp,
                  BitmapFileHeader bh, BitmapInfoHeader bi,
                  unsigned char dataR,
                  unsigned char dataG,
                  unsigned char dataB) {
  int x, y;
  int c;
  unsigned char dummy = '0';
  task_write_header(fp, bh);
  task_write_info(fp, bi);
  for (y = 0; y  iabs(bi-biHeight); y++) {
    c = 0;
    for (x = 0; x  iabs(bi-biWidth); x++) {
      fwrite(&dataB[y  iabs(bi-biWidth) + x], 1, 1, fp);
      fwrite(&dataG[y  iabs(bi-biWidth) + x], 1, 1, fp);
      fwrite(&dataR[y  iabs(bi-biWidth) + x], 1, 1, fp);
      c += 3;
    }
    while (c % 4 != 0) {
      fwrite(&dummy, 1, 1, fp);
      c++;
    }
  }
}

 ------------------------------------------------------------------------- 
struct BMP24 {
  BitmapFileHeader bh;
  BitmapInfoHeader bi;
  unsigned char dataR;
  unsigned char dataG;
  unsigned char dataB;
  unsigned char dataPalette;
};

int BMP24_read(FILE fp, struct BMP24 bmp) {
  if (!bmHeaderCheck(fp, &(bmp-bh)))
    return 0;
  if (!bmInfoHeaderCheck(fp, &(bmp-bi)))
    return 0;
  bmp-dataR = bmp-dataG = bmp-dataB = bmp-dataPalette = NULL;
  if ((bmp-bi).biBitCount == 24) {
    task_read24(fp, &(bmp-bh), &(bmp-bi),
                &(bmp-dataR), &(bmp-dataG), &(bmp-dataB));
  } else if ((bmp-bi).biBitCount == 8) {
    task_read_palette(fp, &bmp-bh, &bmp-bi, &bmp-dataPalette);
    task_read8(fp, &bmp-bh, &bmp-bi,
               &bmp-dataR, &bmp-dataG, &bmp-dataB, bmp-dataPalette);
    xfree(bmp-dataPalette, IDPALETTE);
    bmp-dataPalette = NULL;
  }
  if (!(bmp-dataR && bmp-dataG && bmp-dataB)) {
    xfree(bmp-dataR, IDRGB);
    xfree(bmp-dataG, IDRGB);
    xfree(bmp-dataB, IDRGB);
    return 0;
  }
  return 1;
}

void BMP24_write(FILE fp, struct BMP24 bmp) {
  task_write24(fp, &bmp-bh, &bmp-bi,
               bmp-dataR, bmp-dataG, bmp-dataB);
}

void _BMP24_allocation(struct BMP24 w_bmp, long width, long height) {
  int n;
  w_bmp = xmalloc(sizeof(struct BMP24), IDBMP);
  if (w_bmp == NULL) {
    fprintf(stderr, error(bmp24)n);
    return;
  }
  n = width  3;
  if (n % 4  0)
    n += 4 - (n % 4);
  (w_bmp)-bi.biSizeImage = n  height;
  (w_bmp)-bi.biSize = 40;
  (w_bmp)-bh.bfSize = (w_bmp)-bi.biSizeImage + (w_bmp)-bi.biSize + 14;

  (w_bmp)-bh.bfType1 = 'B';
  (w_bmp)-bh.bfType2 = 'M';
  (w_bmp)-bh.bfReserved1 = 0;
  (w_bmp)-bh.bfReserved2 = 0;
  (w_bmp)-bh.bfOffBits = 54;

  (w_bmp)-bi.biPlanes = 1;
  (w_bmp)-bi.biBitCount = 24;
  (w_bmp)-bi.biCompression = 0;
  (w_bmp)-bi.biHeight = height;
  (w_bmp)-bi.biWidth = width;  
  (w_bmp)-bi.biClrUsed = 0;
  (w_bmp)-bi.biClrImportant = 0;
  (w_bmp)-bi.biXPixPerMeter = 30;
  (w_bmp)-bi.biYPixPerMeter = 30;
  (w_bmp)-dataR = (w_bmp)-dataG = (w_bmp)-dataB = NULL;
  (w_bmp)-dataPalette = NULL;
  for (;;) {
    if (((w_bmp)-dataR = xmalloc(width  height, IDRGB)) == 0)
      break;
    if (((w_bmp)-dataG = xmalloc(width  height, IDRGB)) == 0)
      break;
    if (((w_bmp)-dataB = xmalloc(width  height, IDRGB)) == 0)
      break;
     OK finished 
    return;
  }
   exception 
  xfree((w_bmp)-dataR, IDRGB);
  xfree((w_bmp)-dataG, IDRGB);  
  xfree((w_bmp)-dataB, IDRGB);
  xfree(w_bmp, IDBMP);
  w_bmp = 0;
  return;
}

void BMP24_release(struct BMP24 bmp) {
  if (bmp-dataR) xfree(bmp-dataR, IDRGB);
  if (bmp-dataG) xfree(bmp-dataG, IDRGB);
  if (bmp-dataB) xfree(bmp-dataB, IDRGB);
  if (bmp-dataPalette) xfree(bmp-dataPalette, IDPALETTE);
}

 ------------------------------------------------------------------------- 
#define BUFFSIZE 3  = 2 
char mygetline(FILE fp) {
  static char inbuff[BUFFSIZE];
  char outbuff_malloc, tmpbuff;
  char p, r;
  int fEOL;

  if ((outbuff_malloc = xmalloc(1, ID_GETLINE)) == NULL) {
    return NULL;
  }
  outbuff_malloc = '0';
  fEOL = 0;
  do {
    r = fgets(inbuff, BUFFSIZE, fp);
    if (r == NULL)
      break;
    for (p = inbuff; p != '0'; p++)
      ;
    if ((p - 1) == 'n')
      fEOL = 1;
    if ((tmpbuff = xrealloc(outbuff_malloc, strlen(outbuff_malloc) + strlen(inbuff) + 1, ID_GETLINE)) == NULL) {
      xfree(outbuff_malloc, ID_GETLINE);
      return NULL;
    }
    strcat(tmpbuff, inbuff);
    outbuff_malloc = tmpbuff;
  } while (!fEOL);
  if (strlen(outbuff_malloc)  0) {
    for (p = outbuff_malloc; p != '0'; p++)
      ;
    if ((p - 1) == 'n')
      (p - 1) = '0';
    return outbuff_malloc;
  }
  xfree(outbuff_malloc, ID_GETLINE);
  return NULL;
}

char cutToken(char p, char s) {
  char t, q;
  int flag;
  if (p == 0)
    return 0;
  flag = 0;
  for (q = p; q == ' ' && q != '0'; q++)
    ;
  if (q == '0')
    return 0;
  t = q;
  q++;
  for (; q != ' ' && q != '0'; q++)
    ;
  if (q == '0')
    flag = 1;
  q = '0';
  if (flag)
    s = 0;
  else
    s = q + 1;
  return t;
}

void task_pgm2bmp(FILE fppgm, FILE fpbmp) {
  struct BMP24 bmp;
  long width, height, y, x, d;
  char line, p, q;
  int c;

   header 
  if ((line = mygetline(fppgm)) == 0) {
    fprintf(stderr, cannot read pgm file headern);
    return;
  }
  if (strcmp(line, P2) != 0) {
    fprintf(stderr, pgm header %s not supportedn, line);
    xfree(line, ID_GETLINE);
    return;
  }
  xfree(line, ID_GETLINE);

   width, height 
  if ((line = mygetline(fppgm)) == 0) {
    fprintf(stderr, cannot read pgm file widthheightn);
    return;
  }
  if (sscanf(line, %ld %ld, &width, &height) != 2) {
    fprintf(stderr, pgm widthheight bad formatn);
    xfree(line, ID_GETLINE);
    return;
  }
  xfree(line, ID_GETLINE);

   depth 
  if ((line = mygetline(fppgm)) == 0) {
    fprintf(stderr, cannot read pgm file depthn);
    return;
  }
  if (sscanf(line, %ld, &d) != 1) {
    fprintf(stderr, pgm depth bad formatn);
    xfree(line, ID_GETLINE);
    return;
  }
  xfree(line, ID_GETLINE);

  bmp = 0;
  _BMP24_allocation(&bmp, width, height);
  if (bmp == 0) {
    fprintf(stderr, cannot allocate enough memory(_BMP24_allocation)n);
    return;
  }

  for (y = height - 1; y = 0; --y) {
    if ((line = mygetline(fppgm)) == 0) {
      fprintf(stderr, pgm body bad format(too small  height).n);
      xfree(line, ID_GETLINE);
      return;
    }
    p = line;
    for (x = 0; x  width; x++) {
      if ((q = cutToken(p, &p)) == 0) {
        fprintf(stderr, pgm body bad format(too small  height).n);
        xfree(line, ID_GETLINE);
        BMP24_release(bmp);
        xfree(bmp, IDBMP);
        return;
      }
      c = atoi(q);
      bmp-dataR[y  width + x] = bmp-dataG[y  width + x] = bmp-dataB[y  width + x] = (unsigned char)(255  c  d);
    }
    xfree(line, ID_GETLINE);
  }
  BMP24_write(fpbmp, bmp);
  BMP24_release(bmp);
  xfree(bmp, IDBMP);
}

int main(int argc, char argv) {
  FILE fpbmp, fppgm;
  if (argc != 3) {
    fprintf(stderr, usage %s filenamepgm filenamebmpn, argv[0]);
    exit(-1);
  }
  if ((fppgm = fopen(argv[1], r)) == 0) {
    fprintf(stderr, cannot open the .pgm file for readingn);
    exit(-1);
  }
  if ((fpbmp = fopen(argv[2], w)) == 0) {
    fprintf(stderr, cannot open the .bmp file for writingn);
    fclose(fpbmp);
    exit(-1);
  }
  task_pgm2bmp(fppgm, fpbmp);
  fclose(fpbmp);
  fclose(fppgm);
  xmallocdump();
  return 0;
}
 end 