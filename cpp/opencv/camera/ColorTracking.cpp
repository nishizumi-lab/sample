#include "opencv2\opencv.hpp"
#include "Labeling.h"
using namespace cv;

int main(int argc, char* argv[])
{
    // カメラ映像の幅と高さ
	int w = 640;
	int h = 480;
	Mat im, hsv, mask;					// 画像オブジェクトの作成
	LabelingBS labeling;				// ラベリング関連の変数
	RegionInfoBS *ri;
	short *mask2 = new short[w * h];//ラベリング出力先
	VideoCapture cap(0);				// カメラのキャプチャ
	if (!cap.isOpened()) return -1;		// キャプチャ失敗時のエラー処理

	while (1){
		cap >> im;								// カメラから画像を取得
		cvtColor(im, hsv, CV_BGR2HSV);			// 画像をRGBからHSVに変換
		inRange(hsv, Scalar(150, 70, 70), Scalar(360, 255, 255), mask);	// 色検出でマスク画像の作成
		// 白領域が無い場合のエラー処理
		rectangle(mask, Point(0, 0), Point(1, 1), Scalar(255),-1);
		//ラベリング処理
		labeling.Exec((uchar *)mask.data, mask2, w, h, true, 30);
		//最大の領域を四角で囲む
		ri = labeling.GetResultRegionInfo(0);
		int x1, y1, x2, y2;
		ri->GetMin(x1, y1);
		ri->GetMax(x2, y2);
		rectangle(im, Point(x1, y1), Point(x2, y2), Scalar(255, 0, 0), 3);
		imshow("Camera", im);					// カメラ映像の表示
		imshow("Mask", mask);					// マスク画像の作成
		if (waitKey(30) >= 0){					// 任意のキー入力があれば終了
			break;
		}
	}
	return 0;
}
