#include "opencv2\opencv.hpp"

int main(void){
 
	IplImage *frame = NULL;
	int w  = 640;
	int h = 480;
	double fps = 5.0;

	//カメラの初期化（カメラの選択）
	CvCapture *capture = cvCaptureFromCAM(0);

	//取込サイズの設定
	cvSetCaptureProperty (capture, CV_CAP_PROP_FRAME_WIDTH,  w);
	cvSetCaptureProperty (capture, CV_CAP_PROP_FRAME_HEIGHT, h);

	//ウィンドウの表示
	cvNamedWindow ("Capture", CV_WINDOW_AUTOSIZE);

	CvVideoWriter* VideoWriter = cvCreateVideoWriter("avifile.avi",-1,fps,cvSize(w,h),1);

	while (1) {
		//フレーム画像の取込
		frame = cvQueryFrame (capture);
		//１画面分の書込
		cvWriteFrame(VideoWriter, frame);            
		//画像の表示
		cvShowImage ("Capture", frame);           
		//キー入力待ち（Escキーで終了）
		if (cvWaitKey (1000.0 / fps) == '\x1b')
			break;
	}

	//解放
	cvReleaseCapture (&capture);
	cvDestroyWindow ("Capture");
	cvReleaseVideoWriter(&VideoWriter);

}
