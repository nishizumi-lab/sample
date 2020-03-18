using System;
using OpenCvSharp;

class Program
{
    static void Main(string[] args)
    {
        using (var cap = Cv.CreateCameraCapture(0)) // カメラのキャプチャ
        {
            IplImage im = new IplImage();           // カメラ画像格納用の変数
            while (Cv.WaitKey(1) == -1)             // 任意のキーが入力されるまでカメラ映像を表示
            {
                im = Cv.QueryFrame(cap);            // カメラからフレーム(画像)を取得
                Cv.ShowImage("Test", im);           //  カメラ映像の表示
            }
        }
    }
}
