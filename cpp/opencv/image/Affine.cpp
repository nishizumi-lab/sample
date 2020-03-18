#include "opencv2\opencv.hpp"
  
int main(int argc, char* argv[])
{
	/* 変数の定義 */
	IplImage* im;
	CvMat* rotationMat;
	/* 画像の取得 */
	im = cvLoadImage("test.jpg", CV_LOAD_IMAGE_COLOR);
	/* 回転行列領域の確保 */
	rotationMat = cvCreateMat(2,3 ,CV_32FC1);
	/* 回転行列の計算(90度) */
	cv2DRotationMatrix(cvPoint2D32f(im->height/2, im->width/2), 90, 1, rotationMat);
	/* アフィン変換で回転 */
	cvWarpAffine(im,im,rotationMat);

	/* 画像表示 */
	cvShowImage("Show image", im);
	cvWaitKey(0);
	/* 終了処理 */
	cvDestroyAllWindows();
	cvReleaseImage(&im);
	cvReleaseMat(&rotationMat);
	return 0;
}
