using System;
using System.Linq;

namespace Test
{
        class Program
        {
                static void Main(string[] args)
                {
                        // 最大値を計算
                        double[] data = { 5.1,4.2,3.1,2.2,1.4 };
                        double max = data.Max();
                        Console.WriteLine("最大値：" + max);
                        
                        // 最小値を計算
                        double min = data.Min();
                        Console.WriteLine("最小値：" + min);
                        
                        // 合計を計算
                        for(int i = 0; i < data.Length; i++){
                                sum += data[i];
                        }
                        Console.WriteLine("合計値：" + sum);
                }
        }
}