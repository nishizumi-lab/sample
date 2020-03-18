using System;

namespace sample1 {
    class Program {
        static void Main (string[] args) {
            Calc calc = new Calc ();
            calc.X = 5;
            calc.Y = 10;

            Console.Write ("{0} + {1} = {2}\n", calc.X, calc.Y, calc.Sum);
            // 5 + 10 = 15

            calc.z = 10; // zはpublicだからアクセス可能だが、x, yはprivateなのでアクセス不可
        }
    }
    // 「実装の隠蔽」で作った複素数クラス
    class Calc {
        // 変数は外部から隠蔽(private)
        private double x;
        private double y;
        public double z;

        // xの書き換え・取り出し（プロパティ）
        public double X {
            set { this.x = value; } // valueは外部から代入された値
            get { return this.x; }
        }

        // xの書き換え・取り出し（プロパティ）
        public double Y {
            set { this.y = value; } // valueは外部から代入された値
            get { return this.y; }
        }

        // 和を計算
        public double Sum {
            // 読み取り専用のプロパティ（setブロックを書かない）
            get { return x + y; }
        }
    }
}