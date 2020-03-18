def babble_sort(arr):
    # リストの要素数
    N = len(arr)

    for i in range(N-1):

        cnt = 0  # 交換回数のリセット

        for j in range(0, N-1-i):
            # 前から順に隣り合う要素を比較し、左が右の要素に比べ大きい場合交換
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                cnt = cnt + 1  # 交換回数をカウント

        print(str(i+1)+"回目：", arr)

        # 交換が１度も発生しなければ終了
        if cnt == 0:
            return arr

    
    return arr


# バブルソート１
arr = [7, 2, 5, 3]
print("ソート前：", arr)
babble_sort(arr)
print("ソート後：", arr)

print("-----------")

# バブルソート2
arr = [2, 3, 7, 5]
print("ソート前：", arr)
babble_sort(arr)
print("ソート後：", arr)

"""
ソート前： [7, 2, 5, 3]
1回目： [2, 5, 3, 7]
2回目： [2, 3, 5, 7]
3回目： [2, 3, 5, 7]
ソート後： [2, 3, 5, 7]

-----------

ソート前： [2, 3, 7, 5]
1回目： [2, 3, 5, 7]
2回目： [2, 3, 5, 7]
ソート後： [2, 3, 5, 7]
"""
