#include "opencv2\opencv.hpp"
 
using namespace cv;
 
int main(int argc, char* argv[])
{
 
    Mat im = imread("test.png");    // 入力画像の取得
    int n = 60;                     // 大きいほど階調数が減少
    // 減色処理
    for (int j = 0; j < im.rows; j++) {
        for (int i = 0; i < im.cols; i++) {
            for (int k = 0; k < 3; k++) {
                im.at<vec3b>(j, i)[k] = (im.at<vec3b>(j, i)[k] / n) * n;
            }
        }
    }
 
    imshow("Reduce", im);       // 結果を表示
    waitKey(0);                 // キー入力待機
    return 0;
}
