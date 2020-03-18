#include <iostream>
#include "opencv2\opencv.hpp"

using namespace cv;

int main(int argc, char* argv[])
{

	Mat im = imread("test.png");					// 画像の取得
	if(!im.data) return -1;						// エラー処理

	// 直線の描画(画像，始点，終点，色，線幅、連結する近傍数)
	line(im, Point(100, 100), Point(200, 200), Scalar(0,0,250), 3, 4);

	imshow("Show Image", im);		// 結果表示
	waitKey(0);					// 入力待機
    return 0;

}
