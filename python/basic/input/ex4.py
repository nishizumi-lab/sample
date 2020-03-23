# 行数を取得
print("input number of lines >")
num_lines = int(input())
    
# 1行ずつ取り出し
for i in range(num_lines):
    line = input()
    print("line " + str(i+1) + ":" + line)
