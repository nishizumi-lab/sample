#include <iostream>
#include "opencv2\opencv.hpp"

using namespace cv;

int main(int argc, char* argv[])
{

    Mat im = imread("test.png");		/* 画像の取得 */
    Mat hsv, lab, ycr;
    if(!im.data) return -1;			/* エラー処理 */

	Mat roi(im, Rect(90, 0, 150, 130));	/*トリミング */
	/* 結果表示 */
	imshow("Original", im);
	imshow("ROI", roi);
	waitKey(0);						/* 入力待機 */
    return 0;

}
