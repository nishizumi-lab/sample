#!/bin/bash
var=3


if [ $var -eq 1 ]; then
    echo "i は 1です"
elif [ $var -eq 2 ]; then
    echo "i は 2です"
elif [ $var -eq 3 ]; then
    echo "i は 3です"
else
    echo "i は 1, 2, 3以外の数値です"
fi

# 実行結果は「i は 3です」と表示される。