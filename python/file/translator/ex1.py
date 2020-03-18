# -*- coding: utf-8
from googletrans import Translator

translator = Translator()

jp_words = ['<h2>Scilab on Cloudとは</h2>Scilab（サイラボ）とは、1990年からフランスのINRIAとENPCで開発されているオープンソースの数値計算ソフトです。数値計算機能以外に、信号処理、行列、多項式の数式処理、 グラフ表示なども充実しています。機能やコマンドは、MATLABMATLABによく似ています。（互換性はありません）Scilab on CloudはScilabのクラウド版です。Scilabの計算コマンドやグラフ表示もWebブラウザ上で問題なく使えます。計算処理はクラウドサーバー上で行われるのでスマホでも手軽に使えて便利です。<h2>Scilab on Cloudの使い方</h2>① 下記リンク先からScilab on Cloudの画面を開きます。<blockquote>・<a href="http://cloud.scilab.in/">http://cloud.scilab.in/</a></blockquote>']
en_words = []

for src in jp_words:
    dst = translator.translate(src, src='ja', dest='en')
    en_words.append(dst.text)

print(en_words)  # ['I am Japanese', 'Curry rice I like best']
