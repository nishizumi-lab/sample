using System;
using OpenCvSharp;

class Program
{
    static void Main(string[] args)
    {
        IplImage im = new IplImage("test.png");         // 入力画像を取得
        Cv.CvtColor(im, im, ColorConversion.BgrToHsv);  // RGB色空間からHSV色空間に変換
        Cv.ShowImage("Test", im);                       // 画面に画像を表示
        Cv.WaitKey();                                   // キー入力待機
    }
}
