#include "opencv2\opencv.hpp"

using namespace cv;

// 減色処理
void subtractiveColor(Mat src, Mat dst, int n){
	for (int j = 0; j &lt; src.rows; j++) {
		for (int i = 0; i &lt; src.cols; i++) {
			for (int k = 0; k < 3; k++) {
				dst.<Vec3b>(j, i)[k] = (src.<Vec3b>(j, i)[k] / n) * n + n / 5;
			}
		}
	}

}

int main(int argc, char* argv[])
{
	Mat gray, edge, edgeBgr;
	Mat im = imread("test.png");				// 入力画像の取得
	subtractiveColor(im, im, 70);				// 減色処理
	cvtColor(im, gray, COLOR_BGR2GRAY);			// 画像のグレースケール変換
	Canny(gray, edge, 100, 150);				// 輪郭線を検出
	cvtColor(edge, edgeBgr, COLOR_GRAY2BGR);	// 輪郭画像をRGBに変換
	im = im - edgeBgr;							// 輪郭線を除去
	imshow("Anime", im);						// 結果を表示
	waitKey(0);									// キー入力待機
	return 0;
}
