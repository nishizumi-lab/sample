#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace cv;

int main(int argc, char *argv[])
{
	// 入力画像の取得
	Mat im = imread("test.png",0);
	Mat im2 = im.clone();
	if (im.empty()) return -1;
	// 処理を施したい矩形領域(x,y,w,h)
	Rect roi(100, 100, 200, 200);
	Mat im_roi = im(roi);
	Mat im2_roi = im2(roi);

	// Cannyでエッジ検出
	Canny(im_roi, im2_roi, 50, 200);
	// 結果表示
	imshow("Input", im);
	imshow("Output", im2);
	waitKey(0);
}
