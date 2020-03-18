#include <iostream>
#include "opencv2\opencv.hpp"

using namespace cv;
   
int main(int argc, char* argv[])
{
	Mat im = imread("test.png");	// 画像の取得
	if(!im.data) return -1;		// エラー処理

	// 画像，文字，開始位置，フォント，大きさ，色，線幅，種類
	putText(im, "Moon", Point(50,50), FONT_HERSHEY_TRIPLEX, 1.5, Scalar(0,200,200), 2, CV_AA);

	imshow("Show Image", im);		// 結果表示
	waitKey(0);					// 入力待機
    return 0;
}
