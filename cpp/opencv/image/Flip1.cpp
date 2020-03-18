#include <iostream>
#include "opencv2\opencv.hpp"

using namespace cv;
using namespace std;
  
int main(int argc, char* argv[])
{
	Mat vim, him;					/* 画像格納用 */
    Mat im = imread("test.png");	/* 画像の取得 */

    if(! im.data )
	{								/* 取得失敗時のエラー処理 */
        cout <<  "Could not open or find the image" << std::endl ;
        return -1;
    }
	flip(im, him, 0);				/* 左右反転 */
    imshow("Show image", him);		/* 画像表示 */
    waitKey(0);						/* 入力待機 */
    return 0;
}
