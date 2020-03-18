#include <iostream>
#include "opencv2\opencv.hpp"

using namespace cv;
  
int main(void)
{
	Mat hsv;
	Mat rgb = imread("test.png");	// 画像の取得
	cvtColor(rgb, hsv, CV_RGB2HSV); // RGBからHSVに変換
	imshow("Show image", hsv);	// 画像の表示
	waitKey(0);			// 入力待機
	return 0;
}
