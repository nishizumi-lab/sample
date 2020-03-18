#include "opencv2/opencv.hpp"
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/features2d/features2d.hpp>
#include <opencv2/legacy/legacy.hpp>
#include <opencv2/opencv.hpp>
#include <opencv2/nonfree/nonfree.hpp>
#include <vector>
using namespace cv;

// パノラマ合成
Mat panorama(Mat src1, Mat src2, int width, int height)
{
	// SIFT特徴点の検出と特徴量の計算
	Mat gray1, gray2, des1, des2;
	SiftFeatureDetector detector(2000);
	SiftDescriptorExtractor extrator;
	vector<KeyPoint> kps1, kps2;
	cvtColor(src1, gray1, CV_BGR2GRAY);
	cvtColor(src2, gray2, CV_BGR2GRAY);
	detector.detect(gray1, kps1);
	detector.detect(gray2, kps2);
	extrator.compute(gray1, kps1, des1);
	extrator.compute(gray2, kps2, des2);

	// 特徴点の対応付け
	vector<DMatch> matches;
	BruteForceMatcher< L2<float> > matcher;
	matcher.match(des1, des2, matches);
	vector<Vec2f> pts1(matches.size());
	vector<Vec2f> pts2(matches.size());

	// ホモグラフィの計算
	for (size_t i = 0; i < matches.size(); ++i){
		pts1[i][0] = kps1[matches[i].queryIdx].pt.x;
		pts1[i][1] = kps1[matches[i].queryIdx].pt.y;
		pts2[i][0] = kps2[matches[i].trainIdx].pt.x;
		pts2[i][1] = kps2[matches[i].trainIdx].pt.y;
	}
	Mat H = findHomography(pts1, pts2, CV_RANSAC);

	// ホモグラフィ行列Hを用いてパノラマ合成
	Mat dst;
	warpPerspective(src1, dst, H, Size(width, height));
	for (int y = 0; y < src1.rows; y++){
		for (int x = 0; x < src1.cols; x++){
			dst.at<Vec3b>(y, x) = src2.at<Vec3b>(y, x);
		}
	}
	return dst;
}

int main(int argc, char* argv[])
{
	Mat im1 = imread("test1.png");				// 入力画像1の取得
	Mat im2 = imread("test2.png");				// 入力画像2の取得
	Mat im3 = imread("test3.png");				// 入力画像3の取得
	Mat pr1 = panorama(im1, im2, 1200, 700);	// 画像1,2をパノラマ合成
	Mat pr2 = panorama(im3, pr1, 1200, 700);	// パノラマ写真1と画像3をパノラマ合成
	imshow("Panorama", pr2);					// パノラマ写真を表示
	waitKey(0);									// キー入力待機
	return 0;
}
