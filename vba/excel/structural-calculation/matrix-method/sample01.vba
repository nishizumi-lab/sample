Sub calc_b()

'配列の生成
Dim A(10, 10), v(10), b(10)

'行列サイズを取得
n = Cells(1, 3)

'行列Aの値をセット
For i = 1 To n
    For j = 1 To n
        A(i, j) = Cells(2 + i, 1 + j)
    Next j
Next i

'ベクトルvの値をセット
For i = 1 To n
    v(i) = Cells(2 + i, 1 + n + 1)
Next i

' 行列Aとベクトルvの掛け算を計算
For i = 1 To n
    s = 0
    For j = 1 To n
        s = s + A(i, j) * v(j)
    Next j
    b(i) = s
Next i

'結果を表示
For i = 1 To n
    Cells(2 + i, 1 + n + 2) = b(i)
Next i

End Sub


