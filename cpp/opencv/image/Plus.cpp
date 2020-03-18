#include "opencv2/opencv.hpp"

using namespace cv;

int main(int argc, char* argv[])
{
	Mat im1 = imread("test1.png");	// 入力画像1の取得
	Mat im2 = imread("test2.png");	// 入力画像2の取得
	Mat im = im1 + im2;				// 入力画像1と2の加算
	imshow("TEST", im);				// 結果を表示
	waitKey();						// キー入力待機
	return 0;
}
