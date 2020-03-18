#include <iostream>
#include "opencv2\opencv.hpp"

using namespace cv;
  
int main(int argc, char* argv[])
{
	Mat im = imread("test.png");		// 画像の取得
	if(!im.data) return -1;			// エラー処理

	CascadeClassifier cascade;			// カスケード分類器の取得
	if(!cascade.load("lbpcascade_animeface.xml"))
		return -1;

	// カスケード分類器でアニメ顔の探索
	vector<Rect> faces;
	cascade.detectMultiScale(im, faces, 1.2, 2, CV_HAAR_SCALE_IMAGE, Size(30, 30));

	// アニメ顔探索した結果を描画
	vector<Rect>::const_iterator r = faces.begin();
	for(; r != faces.end(); ++r) {
		rectangle(im, Point(r->x, r->y), Point(r->x + r->width, r->y + r->height),
			Scalar(0,0,200), 3, CV_AA);
	}
	/* 結果表示 */
	imshow("Anime Face Detect", im);
	waitKey(0);						/* 入力待機 */
    return 0;

}
