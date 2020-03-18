# -*- coding: utf-8
from googletrans import Translator

translator = Translator()

jp_words = ['私は日本人です', 'カレーライスが一番好きです']
en_words = []

for src in jp_words:
    dst = translator.translate(src, src='ja', dest='en')
    en_words.append(dst.text)

print(en_words)  # ['I am Japanese', 'Curry rice I like best']
