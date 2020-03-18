#include <iostream>
#include "opencv2\opencv.hpp"

using namespace cv;
    
int main(int argc, char* argv[])
{
	Mat vim, him;					/* 画像格納用 */
    Mat im = imread("test.png");	/* 画像の取得 */

    if(! im.data ) return -1;

	flip(im, vim, 0);				/* 上下反転 */
    imshow("Show image", vim);		/* 画像表示 */
    waitKey(0);						/* 入力待機 */
    return 0;
}
