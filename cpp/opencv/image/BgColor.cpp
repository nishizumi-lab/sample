#include <iostream>
#include "opencv2\opencv.hpp"

using namespace cv;

int main(int argc, char *argv[])
{
	Mat bg(Size(640, 480), CV_8UC3, Scalar(0, 0, 0));	// 背景用の真っ黒な画像を用意
	imshow("Window", bg);								// 背景用画像の表示
	waitKey(0);
}
