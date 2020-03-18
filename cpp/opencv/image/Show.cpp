#include <iostream>
#include "opencv2\opencv.hpp"
using namespace cv;

int main(int argc, char* argv[])
{
    Mat im = imread("test.png");	/* 画像の取得 */

    if(! im.data )return -1;

    imshow("Show image", im);		/* 画像の表示 */
    waitKey(0);						/* 入力待機 */
    return 0;
}
