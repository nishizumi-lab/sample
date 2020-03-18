#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace cv;

int main(int argc, char *argv[])
{
	// 変数宣言
	Mat im;
	// カメラのキャプチャ
	VideoCapture cap(0);
	// キャプチャのエラー処理
	if (!cap.isOpened()) return -1;

	while (1) {
		// カメラ映像の取得
		cap >> im;  
		// 映像の表示
		imshow("Camera", im);
		// キー入力があれば終了
		if (waitKey(30) >= 0) break;
	}
	return 0;
}
