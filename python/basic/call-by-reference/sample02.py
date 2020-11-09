def my_func(list_x):
    print(list_x, id(list_x))  # ② [1, 10] 2315010976704
    list_x.append(100)
    print(list_x, id(list_x))  # ③ [1, 10, 100] 2315010976704

list_y = [1, 10]

print(list_y, id(list_y)) # ①[1, 10] 2315010976704

my_func(list_y) 

print(list_y, id(list_y)) # ④[1, 10, 100] 2315010976704　← ★ 