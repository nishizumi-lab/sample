using System;

namespace Test {
    class Program {
        static void Main () {

            var i = 1;

            while (true) {
                Console.WriteLine (i); // 1, 2, 3, 4, 5
                // iが5を越えたら抜ける
                if (i > 5) {
                    break;
                }
                i++;
            }
        }
    }
}