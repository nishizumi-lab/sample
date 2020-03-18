#include "opencv2\opencv.hpp"
#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
using namespace cv;
  
int main (int argc, char **argv)
{

	Mat im_sobel, im_laplacian, im_canny, im_tmp;
	/* 画像をグレースケールで取得 */
    Mat im = imread("test.jpg", 0);

  /* 画像が無いときのエラー処理 */
  if(! im.data )return -1;
 	/* Sobelフィルタでエッジ検出 */
	Sobel(im, im_tmp, CV_32F, 1, 1);
	convertScaleAbs(im_tmp, im_sobel, 1, 0);
	/* Laplacianフィルタでエッジ検出 */
	Laplacian(im, im_tmp, CV_32F, 3);
	convertScaleAbs(im_tmp, im_laplacian, 1, 0);   
	/* Cannyアルゴリズムでエッジ検出 */
	Canny(im, im_canny, 50, 200);
	/* 画像を表示 */
	imshow("Grayscale", im);
	imshow("Sobel", im_sobel);
	imshow("Laplacian", im_laplacian);
	imshow("Canny", im_canny);
 	/* 画像を保存 */
	imwrite("gray.jpg", im);
	imwrite("sobel.jpg", im_sobel);
	imwrite("laplacian.jpg", im_laplacian);
	imwrite("canny.jpg", im_canny);
	/* 任意のキーが押されるまで待機 */
	waitKey(0);
  return 0;
}
