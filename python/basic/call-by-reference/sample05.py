list_x = [[0] for _ in range(2)]

print(list_x, id(list_x)) # [[0], [0]] 3059227800960

list_x[1].append(1)

print(list_x, id(list_x)) # [[0, 1], [0, 1]] 3059227800960
print(list_x[0], id(list_x[0])) # [0, 1] 3059226258368
print(list_x[1], id(list_x[1])) # [0, 1] 3059226258368

