#include "opencv2\opencv.hpp"

using namespace cv;

int main(int argc, char* argv[])
{
	// 変数の宣言 
	Mat gray;
	Mat im = imread("test.png");					// 画像の取得
	cvtColor(im, gray, CV_BGR2GRAY);				// グレースケール変換
	GaussianBlur(gray, gray, Size(17,17), 2, 2);	// ガウシアンフィルタでノイズ除去
	Canny(gray, gray, 50, 200, 3);
	// Hough変換で直線部分を検出
	HoughLines(gray, lines, 1, CV_PI/180, 200, 0, 0);
	// 検出した直線を描く
	std::vector::iterator it = lines.begin();
	for(; it!=lines.end(); ++it){
        	float rho = (*it)[0], theta = (*it)[1];
        	Point pt1, pt2;
        	double a = cos(theta), b = sin(theta);
        	double x0 = a*rho, y0 = b*rho;
        	pt1.x = saturate_cast(x0 + 1000*(-b));
        	pt1.y = saturate_cast(y0 + 1000*(a));
        	pt2.x = saturate_cast(x0 - 1000*(-b));
        	pt2.y = saturate_cast(y0 - 1000*(a));
		line(OutImg, pt1, pt2, Scalar(0,255,0), 2, CV_AA);
	}
	imshow(" Detect", im);	// 結果表示
	waitKey(0);					// 入力待機
	return 0;
}
