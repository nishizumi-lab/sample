Function calcRx(ByVal R As Double, ByVal num_series As Integer, ByVal num_parallel As Integer) As Variant
    Dim invRx As Double
    Dim i As Integer

    For i = 0 To num_parallel - 1
        invRx = invRx + 1 / R

    Next i
    calcRx = (1 / invRx) * num_series
    
End Function

' ヘッダー名の挿入
Function setHeaderTitle(ByVal num_series As Integer, ByVal num_parallel As Integer)
    Dim i, j, k As Integer
    k = 0
    ' 配列、変数の定義
    Dim names() As Variant
    ReDim names(num_parallel * num_parallel)
    
    For j = 0 To num_series - 1
        For i = 0 To num_parallel - 1
                If (j + 1) * (i + 1) < 9 Then
                    Cells(2, k + 2) = (j + 1) & "直" & (i + 1) & "並"
                    k = k + 1
                End If
        Next i
    Next j
End Function

' 配列の要素確認
Function msgArr(ByVal arr As Variant)
    For Each Var In arr
        msg = msg & Var & ", "
    Next Var
    MsgBox msg
End Function

Function setImpTable(ByVal R As Double, ByVal num_series As Integer, ByVal num_parallel As Integer, ByVal Rext As Variant, ByVal Rline As Double)
    ' 配列、変数の定義
    Dim i, j, k, cnt As Integer

    For j = 0 To UBound(Rext)
        cnt = 0
        For i = 0 To num_series - 1
            For k = 0 To num_parallel - 1
                If (k + 1) * (i + 1) < 9 Then
                    Cells(j + 3, j * cnt + k + 2) = calcRx(R, i + 1, k + 1) + Rline + Rext(j)
                    cnt = cnt + 1
                End If
            Next k
        Cells(j + 3, 1) = Rext(j)
        Next i
    Next j

End Function

Sub macro()
    Dim R, Rx As Double
    Dim Rext As Variant
    Dim num_series As Integer
    Dim num_parallel As Integer

    R = 22
    num_series = 8
    num_parallel = 8
    Rline = 7
    Rext = Array(1, 2, 3, 4, 5, 6, 7, 16, 17, 18, 19, 20, 21, 22, 23, 29, 30, 31, 32, 33, 34, 35, 36, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 67, 68, 69, 70, 71, 72, 73, 79, 80, 81, 82, 83, 84, 85, 86, 95, 96, 97, 98, 99, 100, 101, 102)
    ' 合成抵抗の計算
    Call setImpTable(R, num_series, num_parallel, Rext, Rline)
    
    'E2～●2に直並パターンを挿入
    Call setHeaderTitle(num_series, num_parallel)

End Sub
