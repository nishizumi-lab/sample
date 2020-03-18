#include <opencv2/opencv.hpp>

using namespace cv;

int main(int argc, char *argv[])
{
  Mat hsv, mask;                  // 画像オブジェクトの宣言
  Mat im = imread("map.jpg");		  // 画像の取得
	cvtColor(im, hsv, CV_BGR2HSV);	// 画像をRGBからHSVに変換
	inRange(hsv, Scalar(160, 150, 0), Scalar(190, 255, 255), mask);	// 色検出でマスク画像の作成
	imshow("mask", mask);
	waitKey(0);
	return(0);
}
