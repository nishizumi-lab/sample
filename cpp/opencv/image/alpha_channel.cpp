#include "opencv2\opencv.hpp"

using namespace cv;
  
int main(void)
{
	Mat rgba = imread("test.png",-1);   // 画像の取得(RGBA)
	imshow("Show image", rgba);         // 画像の表示
	waitKey(0);                         // 入力待機
	return 0;
}
