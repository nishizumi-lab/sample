#include <iostream>
#include <opencv2\opencv.hpp>
#include <opencv2/highgui/highgui.hpp>
using namespace cv;

int main(int argc, char *argv[])
{
	// 入力画像をグレースケールで取得
	Mat gray = imread("test.png", 0);
	Mat gray2;
	if (gray.empty()) return -1;
	// ウィンドウを作成
	namedWindow("Test", 1);
	int thMin = 0;
	int thMax = 50;								// トラックバーの初期値
	createTrackbar("Min", "Test", &thMin, 255); // Testウィンドウにトラックバー作成
	createTrackbar("Max", "Test", &thMax, 255); // Testウィンドウにトラックバー作成

	while (1){
		// グレースケール画像の2値化
		threshold(gray, gray2, thMin, thMax, cv::THRESH_BINARY | cv::THRESH_OTSU);
		// 2値画像を画面に表示
		imshow("Test", gray2);
		int iKey = waitKey(50);
		// 何かキーが押されたら終了
		if (iKey >0){ break;}
	}
	return 0;
}
