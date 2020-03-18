using System;
using OpenCvSharp;

class Program
{
    static void Main(string[] args)
    {
        using (IplImage im = new IplImage("test.png"))  // 入力画像の取得
        {
            using (new CvWindow("Test", im))            // 画面に画像を表示
            {
                Cv.WaitKey();                           // キー入力待機
            }
        }
    }
}
