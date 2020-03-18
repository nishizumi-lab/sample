#include <iostream>
#include "opencv2\opencv.hpp"

using namespace cv;
    
int main(int argc, char* argv[])
{
	// 変数の宣言
	double angle = 30;

	Mat im = imread("test.png");	// 画像の取得
	if(!im.data) return -1;		// エラー処理

	// 画像，中心座標，長径・短径，回転角度，円弧開始角度，円弧終了角度，線色，線幅，近傍数
	ellipse(im, Point(200, 200), Size(100, 100), 0, 0, 360, Scalar(200,0,0), 3, 4);
	ellipse(im, Point(300, 300), Size(50, 100), angle, angle-50, angle+150, Scalar(0,200,0), 3, 4);

	imshow("Show Image", im);		// 結果表示
	waitKey(0);					// 入力待機
    return 0;
}
