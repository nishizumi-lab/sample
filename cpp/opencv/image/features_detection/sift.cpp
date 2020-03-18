#include <iostream>
#include <opencv2\opencv.hpp>
#include <opencv2/features2d/features2d.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/nonfree/features2d.hpp>
using namespace cv;
using namespace std;


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

	vector<KeyPoint> keypoints;
	vector<KeyPoint>::iterator itk;

	// SIFT 検出器に基づく特徴点検出(threshold,edgeThreshold)
	SiftFeatureDetector detector(0.05, 10.0);
	detector.detect(gray, keypoints);

	for (itk = keypoints.begin(); itk != keypoints.end(); ++itk) {
		// 検出した特徴点を円で囲む
		circle(im, itk->pt, 1, Scalar(0, 0, 255), -1);
		circle(im, itk->pt, itk->size, Scalar(0, 0, 255), 1, CV_AA);
		if (itk->angle >= 0) {
			Point pt2(itk->pt.x + cos(itk->angle)*itk->size, itk->pt.y + sin(itk->angle)*itk->size);
			line(im, itk->pt, pt2, Scalar(0, 200, 100), 1, CV_AA);
		}
	}
	imshow("Input", im);
	waitKey(0);
}
