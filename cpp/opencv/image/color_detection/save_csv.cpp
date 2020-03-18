#include <opencv2/opencv.hpp>
#include <iostream>

using namespace cv;

class Txt{
private:
public:
	Txt(){}

	double *x, *y, *z;
	int lines;

	// テキストファイルに書き込み
	void saveTxt(char *fname, double rx, double ry)
	{
		// ローカル変数の定義
		FILE *fp;
		// エラー処理
		if ((fp = fopen(fname, "a")) == NULL){
			printf("FILE not open\n");
			exit(1);
		}
		// データ書き込み
		fprintf(fp, "%0.2f\t%0.2f\n", rx, ry);
		fclose(fp);
	}
};

void obstDetection(Mat im, char* fname){
	Txt obst;						// テキストファイルの処理
	Mat hsv, mask;					// 画像オブジェクトの宣言
	cvtColor(im, hsv, CV_BGR2HSV);	// 画像をRGBからHSVに変換
	inRange(hsv, Scalar(160, 150, 0), Scalar(190, 255, 255), mask);	// 色検出でマスク画像の作成
	int h = mask.rows;
	int w = mask.cols;
	for (int y = 0; y < h; y++){
		for (int x = 0; x < w; x++){
			if (mask.data[y * h + x] == 255){
				obst.saveTxt(fname, x, y);		// 赤色部分の座標をテキストファイルに保存
			}
		}
	}
}

int main(int argc, char *argv[])
{
	Mat im = imread("map.jpg");		// 画像の取得
	obstDetection(im, "obst.csv");
	printf("finish");
	return(0);
}
