import itertools

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