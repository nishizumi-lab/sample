import configparser

ini = configparser.ConfigParser()

# iniファイルのロード
ini.read('C:/github/sample/python/basic/file/ini/test.ini', 'UTF-8')

# 中身を出力
print(ini['conf1']['username'])  # admin1
print(ini['conf1']['password'])  # pass1
print(ini['conf2']['username'])  # admin2
print(ini['conf2']['password'])  # pass2
