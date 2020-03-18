#include "opencv2\opencv.hpp"

using namespace cv;
  
int main(void)
{
	Mat im = imread("test.png");    // 画像の取得
	blur(im, im, Size(3,3));        // ぼかしフィルタ
	imshow("Show image", im);	    // 画像の表示
	waitKey(0);                     // 入力待機
	return 0;
}
