# -*- coding: utf-8 -*-
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def main():
    field ="DateTimeOriginal"    # 入手したいExifのデータ種類
    exif_data = []
    im = Image.open("test.jpg")     # 画像の取得
    exif = im._getexif()            # 画像からExifデータを抽出
    # Exifデータから特定のデータのみ抽出
    for id, value in exif.items():
        if TAGS.get(id) == field:
            tag = TAGS.get(id, id),value
            exif_data.extend(tag)

    print exif_data

if __name__ == "__main__":
    main()
