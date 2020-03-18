using OpenCvSharp;

class Program
{
    static void Main(string[] args)
    {
        using (IplImage im = new IplImage("test.png"))      // 入力画像を取得
        // グレースケール画像格納用の変数を作成(チャンネル数は1で縦横サイズは入力画像と同じ)
        using (IplImage gray = Cv.CreateImage(new CvSize(im.Width, im.Height), BitDepth.U8, 1))
        {
            Cv.CvtColor(im, gray, ColorConversion.BgrToGray); // グレースケール変換
            using (new CvWindow("Test", gray))                // 画面に画像を表示
            {
                Cv.WaitKey();                               // キー入力待機
            }
        }
    }
}
