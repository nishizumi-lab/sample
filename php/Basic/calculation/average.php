<?php

// 配列を宣言・初期化
$datas = array(1, 2, 3, 4, 5);

// 合計
$sum = array_sum($datas);
print $sum; // 15
print(PHP_EOL);

// 平均
$average = $sum/count($datas);
print $average; // 3
print(PHP_EOL);

// 最大値
$max = max($datas);
print $max; // 5
print(PHP_EOL);

// 最小値
$min = min($datas);
print $min; // 1
print(PHP_EOL);