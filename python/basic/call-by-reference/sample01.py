def my_func(x):
    print(x, id(x))  # ② 1   140703210804896 
    x = x * 100
    print(x, id(x))  # ③ 100 140703210808064 

y = 1

print(y, id(y)) # ①1   140703210804896

my_func(y) 

print(y, id(y)) # ④1   140703210804896