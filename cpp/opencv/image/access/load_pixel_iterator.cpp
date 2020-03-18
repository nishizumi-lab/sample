#include <iostream>
#include "opencv2\opencv.hpp"

using namespace cv;

int main(int argc, char *argv[])
{
	Mat im = imread("test.jpg");					 // 画層の読み込み	
	MatIterator_<Vec3b> itd = im.begin<Vec3b>();
	MatIterator_<Vec3b> itd_end = im.end<Vec3b>();
	for(int i=0; itd != itd_end; ++itd, ++i) {
		Vec3b bgr = (*itd);                           // 画素値の取得
    		printf("%d,%d,%d\n", bgr[0], bgr[1], bgr[2]); // 画素値の表示
	}
	return 0;
}
