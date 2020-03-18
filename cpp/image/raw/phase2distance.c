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
  
/*  距離画像の作成 */
void calcDisplace(unsigned char *im0, unsigned char *im1, long size, double lamda, int zmax)
{
    /* 変数の定義*/
    unsigned char   *distance, *ip;
    float   *distance_f, *p;
	double numer, denom;
    long    i;
    /* 位相画像(1画素4byte)のメモリ確保*/
    distance_f  = (float *)malloc(size * 4);
    /* 位相画像(1画素1byte)のメモリ確保*/
    distance = (unsigned char *)malloc(size);
    ip = distance;
    p = distance_f;
    /* 奥行きの計算*/
    for(i = 0; i < size; i++){
		*im0 = *im0 * (pi*2.0/254);
		*im1 = *im1 * (pi*2.0/254);
        if(*im1 != *im0)
        {
			numer = abs((double)(*im0) - (double)(*im1));
			denom = 2*2*pi;
			if(denom < 0){ denom = denom + 2.0*pi; }
            *p =  lamda*( numer ) / ( denom );
        }
        else{ *p=0; }
        /* 距離を輝度に変換*/
        *ip = *p* (254/zmax);
        im0++;
        im1++;
        ip++;
        p++;
    }
    SaveImg((unsigned char *)distance, size, "distance.raw"); 
}
  
/*  メイン文 */
int main( )
{
    /* 変数の定義 */
    unsigned char   *im, *im0, *im1;
    long    size;
    FILE    *fp;
    /* 画像サイズ(横*縦) */
    size = 320 * 240;
    /* 実数画像のメモリ 確保*/
    im0 = (unsigned char *)malloc(size);
    im1 = (unsigned char *)malloc(size);
    /* 位相分布画像の取得 */
    LoadImg(im0, size, "p0.raw");
    LoadImg(im1, size, "p1.raw");
    /* 距離画像の作成 */
    calcDisplace(im0, im1, size, 633, 150);
    printf("Success!\n");
    return 0;
}
