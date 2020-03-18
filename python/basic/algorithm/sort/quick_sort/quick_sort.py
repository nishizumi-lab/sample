import sys

def quick_sort(arr):
    # 左右２つに分割したデータを格納するリスト
    left_arr = []
    right_arr = []

    # 要素数長が１以下なら終了
    if len(arr) <= 1:
        return arr

    # 先頭要素を軸要素（基準値）に指定
    pivot = arr[0]
    pivot_count = 0

    # 左右２つのグループに分割
    for ele in arr:
        if ele < pivot:
            left_arr.append(ele)
        elif ele > pivot:
            right_arr.append(ele)
        # 基準値と同じなら、その個数をカウント
        else:
            pivot_count += 1

    # 左右２つに分割したリストに対して、再帰的に関数を呼び出して繰り返す
    left_arr = quick_sort(left_arr)
    right_arr = quick_sort(right_arr)

    # ソートしたら分割したリストを結合（ピポッドはカウントされた個数だけ中央に挿入）
    return left_arr + [pivot] * pivot_count + right_arr


# クイックソート１
arr = [2, 3, 7, 5]
print("ソート前：", arr)
sorted_arr = quick_sort(arr)
print("ソート後：", sorted_arr)

print("-----------")

# クイックソート2
arr = [9, 5, 8, 2, 8, 9, 7]
print("ソート前：", arr)
sorted_arr = quick_sort(arr)
print("ソート後：", sorted_arr)

"""
ソート前： [2, 3, 7, 5]
ソート後： [2, 3, 5, 7]

-----------

ソート前： [9, 5, 8, 2, 8, 9, 7]
ソート後： [2, 5, 7, 8, 8, 9, 9]
"""
