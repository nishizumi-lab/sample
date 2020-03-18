#include <iostream>
#include "opencv2\opencv.hpp"

using namespace cv;

int main(int argc, char *argv[])
{
	Mat im = imread("test.jpg");							// 画層の読み込み	
	for (int y = 0; y < im.rows; y++) {
		Vec3b* ptr = im.ptr<Vec3b>(y);						// ポインタの取得
		for (int x = 0; x < im.cols; x++) {
			Vec3b bgr = ptr[x];								// 画素値(blue, green, red)の取得
			printf("%d,%d,%d\n", bgr[0], bgr[1], bgr[2]);	// 取得した画素値の表示
		}
	}
	return 0;
}
