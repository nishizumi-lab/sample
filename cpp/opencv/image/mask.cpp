#include "opencv2\opencv.hpp"

using namespace cv;
  
int main (int argc, char **argv)
{
	Mat gray;
	Mat im = imread("test.jpg");		// 入力画像を読み込み
	Mat mask = imread("mask.jpg");		// マスク画像を読み込み
	bitwise_and(im, im, mask);
	imshow("Result", im);		    	// ウィンドウに画像表示
	waitKey(0);				            // 任意のキーが押されるまで待機
	return 0;
}
