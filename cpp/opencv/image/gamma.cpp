#include "opencv2\opencv.hpp"

using namespace cv;
  
int main(int argc, char* argv[])
{
	Mat im = imread("test.png");	  // 画像の取得
    vector<Mat> rgb;
    split(im, rgb);//チャンネルを分離する
    float gain[] = {-0.5f, 2.0f, 6.0f};    // コントラスト調整用（各チャンネルでのシグモイド関数のゲイン）
    float sigma[] = {0.5f, 0.8f, 0.3f};    // ガンマ補正用（各チャンネルでのシグマ値）
    uchar lut[256];
    
    for (int ch = 0; ch < 3; ch++) {
        Mat dst;                 // 結果保存用のMat型配列
        Mat src = rgb[ch];
        // ルックアップテーブル作成
        for (int i = 0; i < 256; i++){
            lut[i] = 255.0 / (1+exp(-gain[ch]*(i-128)/255));
        }
        LUT(src, Mat(Size(256, 1), CV_8U, lut), result);
        // ガンマ補正
        for (int i = 0; i < 256; i++){
            lut[i] = pow(1.0*i/255, 1.0/sigma[ch]) * 255;
        }
        LUT(dst, Mat(Size(256, 1), CV_8U, lut), dst);
        rgb[ch] = dst;                                   // ガンマ補正した結果を保存(1チャンネルずつ)
    }
    // チャンネルを合成する
    Mat im2;
    merge(rgb, im2);
	imshow("Show image", im2);  // 画像の表示
	waitKey(0);	                // 入力待機
	return 0;
}
