#include "opencv2\opencv.hpp"

using namespace cv;

int main(int argc, char *argv[])
{
	Mat im, gray, bg, diff, dst;
	int th = 20;					// 2値化の閾値
	VideoCapture cap(0);
	cap >> im;
	cvtColor(im, bg, CV_BGR2GRAY); // 最初のフレームを背景画像に設定

	while (1){
		cap >>im;
		cvtColor(im, gray, CV_BGR2GRAY);
		absdiff(gray, bg, diff);						// 現フレームと背景画像の差分を取得
		threshold(diff, dst, th, 255, THRESH_BINARY);	// 差分画像を閾値thで2値化
		imshow("Camera", dst);							// 結果を表示
		if (waitKey(1) >= 32){							// スペースキーが押されたら背景更新
			cvtColor(im, bg, CV_BGR2GRAY);
		}
		if (waitKey(1) == 27){							// Escキーが入力されたら終了
			break;     
		}

	}
	return 0;
}
