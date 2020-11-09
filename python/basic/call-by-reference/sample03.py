import copy

def my_func(list_x):
    print(list_x, id(list_x))  # ② [1, 10] 2804715309632

    # オブジェクトをコピーして変更を加える
    list_x_copy = copy.deepcopy(list_x)
    list_x_copy.append(100)
    print(list_x, id(list_x))  # ③ [1, 10] 2804715309632
    print(list_x_copy, id(list_x_copy)) # ④ [1, 10, 100] 2804715310656
    
    return list_x_copy

list_y = [1, 10]

print(list_y, id(list_y)) # ①　[1, 10] 2804715309632

list_y_copy = my_func(list_y) 

print(list_y, id(list_y)) # ⑤ [1, 10] 2804715309632
print(list_y_copy, id(list_y_copy)) # ④　[1, 10, 100] 2804715310656