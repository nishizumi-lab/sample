#include <iostream>
#include "opencv2\opencv.hpp"

using namespace cv;

int main(int argc, char *argv[])
{
	Mat im(Size(300, 300), CV_8UC3, Scalar(0, 0, 0));	// 真っ黒(全ての画素値が0)なMat型配列(画像データ)を作成
	imwrite("test.jpg", im);								          // Mat型配列(画像データ)をJPG形式で保存
	waitKey(0);
}
