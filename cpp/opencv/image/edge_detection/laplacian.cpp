#include "opencv2\opencv.hpp"

using namespace cv;
  
int main (int argc, char **argv)
{
	Mat gray;
	Mat im = imread("test.jpg");		// 画像を読み込み
	cvtColor(im, gray, CV_BGR2GRAY);	// グレースケール変換
	Laplacian(gray, gray, CV_32F, 3);	// Laplacianフィルタでエッジ検出
	convertScaleAbs(gray, gray, 1, 0);
	imshow("Sobel", gray);              // ウィンドウに画像表示
	waitKey(0);                         // 任意のキーが押されるまで待機
	return 0;
}
