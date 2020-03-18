#include <iostream>
#include "opencv2\opencv.hpp"

using namespace cv;
  
int main(void)
{
	Mat gray;
  Mat im = imread("test.png");	    // 画像の取得
  if(! im.data )return -1;
  cvtColor(im, gray, CV_RGB2GRAY);  // グレースケール変換
  imshow("Show image", gray);		    // 画像の表示
  waitKey(0);						            // 入力待機
  return 0;
}
