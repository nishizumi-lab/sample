#include <iostream>
#include "opencv2\opencv.hpp"

using namespace cv;
  
int main(void)
{
	Mat rgb;
	Mat hsv = imread("test.png");	  // 画像の取得
	cvtColor(hsv, rgb, CV_HSV2RGB); //HSVからRGBに変換
	imshow("Show image", rgb);	    // 画像の表示
	waitKey(0);			                // 入力待機
	return 0;
}
