
#include "opencv2\opencv.hpp"

using namespace cv;
 
int main(int argc, char* argv[])
{
    Mat im = imread("test.png");	/* 画像の取得 */
    cv::resize(im, im, Size(), 0.1, 0.1);			    // 画像を補完なしで1/10に縮小
    cv::resize(im, im, Size(), 10, 10, cv::INTER_NN);	// 画像を補完なしで10倍に拡大(元のサイズ)
	/* 結果表示 */
	imshow("Mosaic", im);
	waitKey(0);
    return 0;						/* 入力待機 */

}
