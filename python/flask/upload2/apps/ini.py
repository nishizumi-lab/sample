from flask import Flask, render_template, url_for, request, redirect, Blueprint
import os
import io
import base64
import configparser

# Blueprintオブジェクトを生成
app = Blueprint('ini', __name__)

# ini にアクセスされた場合の処理
@app.route('/ini', methods=['GET', 'POST'])
def ini():
  username = ""
  password = ""
  message = "hello!"
  INPUT_NAME = 'file1'
  HTML_PATH = 'ini.html'
  TITLE = "TEST PAGE"

  if request.method == 'POST':
    filebuf = request.files[INPUT_NAME].read()
    int_texts = filebuf.decode('utf-8')
    config = configparser.ConfigParser()
    try:
        config.read_string(int_texts)
        message = "Loaded ini file"
        username = config.get('conf1', 'username')
        password = config.get('conf1', 'password')
    except:
      message = "not ini file"
      username = ""
      password = ""

    return render_template(HTML_PATH,
                           title=TITLE,
                           username=username,
                           password=password,
                           message=message,
                           input_name=INPUT_NAME)

  else:
    return render_template(HTML_PATH,
                           title=TITLE,
                           username=username,
                           password=password,
                           message=message,
                           input_name=INPUT_NAME)

