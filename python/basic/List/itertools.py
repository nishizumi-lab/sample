import itertools


# 3P2の順列：1, 2, 3の玉が入った袋から2つの玉を取り出す
# 第2引数を省略すると3P3 (= 3!)になる
num_list = [1, 2, 3]
new_list = []

for num in itertools.permutations(num_list, 2):
    new_list.append(num)

print(new_list)
# [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]


# 1, 2, 3と書かれた玉が入った袋から、2つの玉を区別なく同時に取り出す (3C2の組み合わせ)
num_list = [1, 2, 3]
new_list = []
for num in itertools.combinations(num_list, 2):
    new_list.append(num)

print(new_list)
# [(1, 2), (1, 3), (2, 3)]


# 重複順列：1, 2, 3と書かれた玉が入った袋から、2つの玉を取り出す（ただし取り出した玉はまた袋に戻す）
num_list = [1, 2, 3]
new_list = []
for num in itertools.product(num_list, repeat=2):
    new_list.append(num)

print(new_list)
# [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]


# 重複組合せ:1, 2, 3と書かれた玉が2セット入った袋から、2つの玉を区別なく同時に取り出す
num_list = [1, 2, 3]
new_list = []
for num in itertools.combinations_with_replacement(num_list, 2):
    new_list.append(num)

print(new_list)
# [(1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]


# 2つの集合の直積
sign_list = ['a', 'b', 'c']
num_list = [1, 2, 3]
new_list = []
for pairs in itertools.product(sign_list, num_list):
    new_list.append(pairs)

print(new_list)
# [('a', 1), ('a', 2), ('a', 3), ('b', 1), ('b', 2), ('b', 3), ('c', 1), ('c', 2), ('c', 3)]


num_list = [1, 2, 3]
new_list = []

for i in range(1, len(num_list)+1):
    els = [list(x) for x in itertools.combinations(num_list, i)]
    new_list.extend(els)

print(new_list)
# [[1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]


new_sum_list = [sum(x) for x in new_list]
print(new_sum_list)
# [1, 2, 3, 3, 4, 5, 6]