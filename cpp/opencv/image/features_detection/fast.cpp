#include <iostream>
#include <opencv2\opencv.hpp>
#include <opencv2/features2d/features2d.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/nonfree/features2d.hpp>
using namespace cv;

int main(int argc, char *argv[])
{
	// 入力画像の取得
	Mat im = imread("test.png", 1);
	if (im.empty()) return -1;
	// グレースケール変換
	Mat gray;
	cvtColor(im, gray, CV_RGB2GRAY);
	// グレースケール画像の正規化
	normalize(gray, gray, 0, 255, NORM_MINMAX);

	// FAST検出器に基づく特徴点検出
  vector<KeyPoint> kps;
  FAST(gray, kps, 105, true);
  vector<KeyPoint>::iterator it_kp = kps.begin();
  for(; it_kp!=kps.end(); ++it_kp) {
    circle(im, Point(it_kp->pt.x, it_kp->pt.y), 1, Scalar(0,0,200), -1);
    circle(im, Point(it_kp->pt.x, it_kp->pt.y), 8, Scalar(0,0,200));
  }
	imshow("Result", im);
	waitKey(0);
}
