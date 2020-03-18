using System;

namespace Test {
    class Program {
        static void Main () {

            // 変数の宣言・初期化
            int i = 10;
            int j = 0;

            // iをjに代入した後、iを1増やす
            i = 10;
            j = 0;
            j = i++;　
            Console.WriteLine (i); // 11
            Console.WriteLine (j); // 10

            // iをjに代入した後、iを1減らす
            i = 10;
            j = 0;
            j = i--;　
            Console.WriteLine (i); // 9
            Console.WriteLine (j); // 10

            // iを1増やした後、jに代入　
            i = 10;
            j = 0;
            j = ++i;　
            Console.WriteLine (i); // 11
            Console.WriteLine (j); // 11

            // iを1減らした後、jに代入
            i = 10;
            j = 0;
            j = --i;　
            Console.WriteLine (i); // 9
            Console.WriteLine (j); // 9
        }
    }
}