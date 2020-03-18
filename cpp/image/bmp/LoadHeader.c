#include <stdio.h>
#include <stdlib.h>

// ビットマップ画像の読み取り
int loadBmp(char fn[], int *w, int *h, int *bit){
	FILE			*fp;			// ファイルポインタの宣言
	unsigned char	hdr[54];	// ヘッダ格納用の配列
	int i;							// ループ用変数
	
	fp=fopen(fn,"rb");		// bmpファイルをバイナリモードで読み取り
	
	// 画像ファイルが見つからない場合のエラー処理
	if(fp==NULL){
		printf("Not found : %s \n", fn);	exit(-1);
	}
	
	// ヘッダ情報の読み込み
	for(i=0; i<54; i++)		hdr[i] = fgetc(fp);   
	
	// 画像がビットマップで無い場合のエラー処理
	if(!(hdr[0]=='B'&& hdr[1]=='M')){
		printf("%Not BMP file : &s \n", fn);  exit(-1);
	}
	
	// ヘッダ情報から画像の幅、高さ、ビットの深さを抽出
	*w = hdr[18] + hdr[19]*256;
	*h = hdr[22] + hdr[23]*256;
	*bit = hdr[28];
	fclose(fp);					// ファイルを閉じる
	return 0;
}


int main(void){
	int	w, h, bit;			// 変数の宣言
	// bmp画像の読み込み
	loadBmp("test.bmp", &w, &h, &bit);	
	// bmp画像の幅，高さ，ビットの深さ, チャンネル数を表示
	printf(".....Width：%d\n", w);
	printf(".....Hight：%d\n", h);
	printf(".....Bit：%d\n", bit);
	printf(".....Channel : %d", bit/8);
  	return 0;
}
