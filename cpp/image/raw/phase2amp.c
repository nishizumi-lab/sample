#include    <stdio.h>
#include    <stdlib.h>
#include    <math.h>
#define     pi      (double)(3.141592653579)
 
/*  画像の読み込み */
void LoadImg(unsigned char *im, long size, char *fn)
{
    FILE    *fp;
 
    fp = fopen(fn, "rb");
    if(fp == 0L){
        printf("%s not open\n", fn);
        exit(1);
    }
    printf("load %s....\n", fn);
    fread(im, size, 1, fp);
    fclose(fp);
}
 
/*  画像の保存 */
void SaveImg(unsigned char *im, long size, char *fn)
{
    FILE    *fp;
    fp = fopen(fn, "wb");
    if( fp == 0L ){
        printf("%s not open\n", fn);
        exit(1);
    }
    fwrite(im, size, 1L, fp);
    fclose(fp);
}
 
/*  位相分布画像の作成 */
void AmpImg(unsigned char *im0, unsigned char *im1, unsigned char *im2, unsigned char *im3, long size)
{
    /* 変数の定義*/
    unsigned char   *im, *p;
    long    i;
    /* 位相画像(1画素1byte)のメモリ確保*/
    im = (unsigned char *)malloc(size);
    p = im;
    /* 振幅の計算*/
    for(i = 0; i < size; i++){
        *p = sqrt( (*im3-*im1)*(*im3-*im1) + (*im2-*im0)*(*im2-*im0) );
        im0++;
        im1++;
        im2++;
        im3++;
        p++;
    }
    /* 振幅画像の生成（整数）*/
    SaveImg((unsigned char *)im, size, "image.raw");   
}
 
/*  メイン文 */
int main( )
{
    /* 変数の定義 */
    unsigned char   *im0, *im1, *im2, *im3;
    long    size;
    FILE    *fp;
    /* 画像サイズ(横*縦) */
    size = 640 * 480;
    /* 画像のメモリ 確保*/
    im0 = (unsigned char *)malloc(size);
    im1 = (unsigned char *)malloc(size);
    im2 = (unsigned char *)malloc(size);
    im3 = (unsigned char *)malloc(size);
    /* 画像の取得 */
    LoadImg(im0, size, "0.raw");
    LoadImg(im1, size, "1.raw");
    LoadImg(im2, size, "2.raw");
    LoadImg(im3, size, "3.raw");
    /* 位相分布画像の作成 */
    AmpImg(im0, im1, im2, im3, size);
    printf("Success!\n");
    return 0;
}
