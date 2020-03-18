#include "opencv2\opencv.hpp"

using namespace cv;
  
int main (int argc, char **argv)
{
	Mat gray;
	Mat im = imread("test.jpg");		// 画像を読み込み
	cvtColor(im, gray, CV_BGR2GRAY);	// グレースケール変換
	Canny(gray, gray, 50, 200);	        // Cannyでエッジ検出
	imshow("Edge", gray);               // ウィンドウに画像表示
	waitKey(0);                         // 任意のキーが押されるまで待機
	return 0;
}
