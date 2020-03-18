#include <iostream>
#include "opencv2\opencv.hpp"

using namespace cv;

int main(int argc, char* argv[])
{
	Mat gray = imread("test.png",0);	// 画像の取得
	Mat gray2;
	if(!gray.data) return -1;		// エラー処理
	// ヒストグラム平均化
	equalizeHist(gray, gray2);
	imshow("Input", gray);		// 結果表示
	imshow("Output", gray2);		// 結果表示
	waitKey(0);					// 入力待機
    return 0;
}
