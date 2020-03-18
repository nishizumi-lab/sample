using System;
using OpenCvSharp;
using OpenCvSharp.Blob;
class Program
{
    static void Main(string[] args)
    {
        CvScalar hsv_min = Cv.RGB(150, 70, 70);     // 抽出するHSV色領域の下限
        CvScalar hsv_max = Cv.RGB(360, 255, 255);   // 抽出するHSV色領域の上限
        var cap = Cv.CreateCameraCapture(0);        // カメラのキャプチャ
        IplImage im = new IplImage();               // カメラ画像(フレーム)格納用
        IplImage hsv = Cv.CreateImage(new CvSize(640, 480), BitDepth.U8, 3);    // HSV画像格納用
        IplImage mask = Cv.CreateImage(new CvSize(640, 480), BitDepth.U8, 1);   // マスク画像格納用
        while (Cv.WaitKey(1) == -1)                 // 任意のキーが入力されるまでカメラ映像を表示
        {
            im = Cv.QueryFrame(cap);                        // カメラからフレーム(画像)を取得
            Cv.CvtColor(im, hsv, ColorConversion.BgrToHsv); // RGB色空間からHSV色空間に変換
            Cv.InRangeS(hsv, hsv_min, hsv_max, mask);       // 指定した範囲内の色抽出(マスクの作成)
            Cv.Dilate(mask, mask, null, 1);                 // 膨張処理
            Cv.Erode(mask, mask, null, 1);                  // 収縮処理
            Cv.Erode(mask, mask, null, 1);                  // 収縮処理
            Cv.Dilate(mask, mask, null, 1);                 // 膨張処理
            // エラー処理(マスクに白領域が全くないとラベリング処理でエラー)
            Cv.Ellipse(mask, new CvPoint(0, 0), new CvSize(1, 1), 0, 0, 360, CvColor.White, -1); 
            CvBlobs blobs = new CvBlobs(mask);              // マスク画像のラベリング処理
            CvBlob maxBlob = blobs.LargestBlob();           // 面積が最大のラベルを抽出
            CvPoint pt = maxBlob.Centroid;                  // 面積が最大のラベルの重心座標を取得
            // 重心点に十字線を描く
            Cv.Line(im, new CvPoint(pt.X, pt.Y - 50), new CvPoint(pt.X, pt.Y + 50), new CvColor(0, 255, 0), 5);
            Cv.Line(im, new CvPoint(pt.X - 50, pt.Y), new CvPoint(pt.X + 50, pt.Y), new CvColor(0, 255, 0), 5);
            Cv.ShowImage("Frame", im);                      // 画面にフレームを表示
            Cv.ShowImage("Mask", mask);                     // 画面にマスク画像を表示
        }
    }
}
