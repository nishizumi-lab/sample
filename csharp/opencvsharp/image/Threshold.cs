using System;
using OpenCvSharp;

class Program
{
    static void Main(string[] args)
    {
        using (IplImage im = new IplImage("test.png"))              // 入力画像を取得
        using (IplImage gray = Cv.CreateImage(new CvSize(im.Width, im.Height), BitDepth.U8, 1)) // グレースケール画像格納用の変数
        {
            Cv.CvtColor(im, gray, ColorConversion.BgrToGray);       // グレースケール変換
            Cv.Threshold(gray, gray, 0, 255, ThresholdType.Otsu);   // グレースケール画像を2値化
            using (new CvWindow("Test", gray))                      // 結果を表示
            {
                Cv.WaitKey();                                       // キー入力待機
            }
        }
    }
}
