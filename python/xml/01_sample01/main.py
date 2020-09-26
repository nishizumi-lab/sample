import xml.etree.ElementTree as ET


# XMLデータの読み込み
tree = ET.parse('C:/github/sample/python/xml/00_sample_data/rss.xml') 
root = tree.getroot()

# 最上位階層のタグ・中身
print(root.tag,root.attrib)
"""
rss {'version': '2.0'}
"""

# 子階層のタグ・中身
for child in root:
    print(child.tag, child.attrib)

"""
channel {}
"""


# 要素「title」のデータを1つずつ取得
for title in root.iter('title'):
    print(title.text)

"""
Example Title1
HogeHoge Item Title
"""


# 配列の要素番号でデータを取得
print(root[0])
print(root[0][0])
print(root[0][1])
print(root[0][2])
print(root[0][0].text)
print(root[0][1].text)
print(root[0][2].text)

"""
<Element 'channel' at 0x00000219D6A93BD0>
<Element 'title' at 0x00000219D6AC0AE0>
<Element 'description' at 0x00000219D6AC0B30>
<Element 'link' at 0x00000219D6AC0BD0>
Example Title1
HogeHoge Description
http://example.ex/
"""