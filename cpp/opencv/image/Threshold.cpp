#include <iostream>
#include "opencv2\opencv.hpp"

using namespace cv;

int main(int argc, char* argv[]){
	Mat gray;						// 画像格納用
	Mat im = imread("test.png");	// 画像の取得
	cvtColor(im, gray, CV_RGB2GRAY);// グレースケール変換
	threshold(gray, gray, 0, 255, cv::THRESH_BINARY|cv::THRESH_OTSU);	// 2値化
	imshow("Show image", gray);		// 画像の表示
	waitKey(0);						// 入力待機
	return 0;
}
