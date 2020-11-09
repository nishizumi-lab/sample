def my_func(x, list_x=[]):
    list_x.append(x)
    return list_x

list_y1 = my_func(1)

print(list_y1, id(list_y1)) # [1] 1695101037504

list_y2 = my_func(1)

print(list_y2, id(list_y2)) # [1, 1] 1695101037504