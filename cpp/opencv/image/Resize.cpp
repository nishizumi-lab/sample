#include <iostream>
#include "opencv2\opencv.hpp"

using namespace cv;
using namespace std;
 
int main(int argc, char* argv[])
{

    Mat im = imread("test.png");	/* 画像の取得 */
    Mat im2, im3;
    if(!im.data) return -1;

	/* サイズ変更(1/2) */
    cv::resize(im, im2, Size(), 0.5, 0.5);			/* バイリニア補間で1/2倍 */
    cv::resize(im, im3, Size(), 2, 2, INTER_CUBIC);	/* バイキュービック補間で2倍 */
	/* 結果表示 */
	imshow("resize1", im2);
	imshow("resize2", im3);
	waitKey(0);
    return 0;						/* 入力待機 */

}
