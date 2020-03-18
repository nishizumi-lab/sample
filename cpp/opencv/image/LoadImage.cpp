#include <iostream>
#include "opencv2\opencv.hpp"

using namespace cv;

int main(int argc, char *argv[])
{
	Mat im = imread("test.jpg");	// カラー(RGBの3チャンネル)で読み込み	
	Mat im = imread("test.jpg", 1);	// カラー(3チャンネル)で読み込み
	Mat im = imread("test.jpg", 0);	// グレースケール(3チャンネル)で読み込み
	Mat im = imread("test.jpg", -1);// カラー(RGBAの4チャンネル)で読み込み
}
