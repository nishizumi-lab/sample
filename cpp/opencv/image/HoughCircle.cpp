#include <iostream>
#include "opencv2\opencv.hpp"

using namespace cv;

int main(int argc, char* argv[])
{
	// 変数の宣言 
	Mat gray;

	Mat im = imread("test.png");					// 画像の取得
	if(!im.data) return -1;						// エラー処理

	cvtColor(im, gray, CV_BGR2GRAY);				// グレースケール変換
	GaussianBlur(gray, gray, Size(17,17), 2, 2);	// ガウシアンフィルタでノイズ除去

	// Hough変換で円部分を検出
	vector<Vec3f> circles;
	HoughCircles(gray, circles, CV_HOUGH_GRADIENT, 1, 100, 20, 50);
	vector<cv::Vec3f>::iterator it = circles.begin();

	// 検出した円を描く
	for(; it!=circles.end(); ++it) {
		Point center(saturate_cast<int>((*it)[0]),saturate_cast<int>((*it)[1]));
		int radius = saturate_cast<int>((*it)[2]);
		circle(im, center, radius, Scalar(0,0,255), 2);
	}

	imshow("Circle Detect", im);	// 結果表示
	waitKey(0);					// 入力待機
    return 0;

}
