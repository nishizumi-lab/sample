# -*- coding: uTf-8 -*-
import glob
import os
from chardet.universaldetector import UniversalDetector


class FilEdit():
    # 相対パス -> 絶対パス
    def listup_files(self, path):
        yield [os.path.abspath(p) for p in glob.glob(path)]

    # ファイルの文字コードを取得
    def get_file_encoding(self, file_path):
        detector = UniversalDetector()
        with open(file_path, mode='rb') as f:
            for binary in f:
                detector.feed(binary)
                if detector.done:
                    break
        detector.close()
        return detector.result['encoding']

    def get_paths(self, dir_path):
        file_abs_paths = []

        for dir_path, subdir_paths, subfile_paths in os.walk(dir_path):
            for filepath in subfile_paths:
                file_abs_paths.append(dir_path + '\\' + filepath)

        return {"file_abs_path": file_abs_paths,
                "subdir_path": subdir_paths,
                "subfile_path": subfile_paths
                }

    # キーワード検索
    def search_words(self, filepath, keyword, ignore_exts=None):
        print(filepath + "をロードします")
        encoding = self.get_file_encoding(filepath)
        # ファイルの中身を1行ずつ読み込んでリストに格納
        with open(filepath, mode='r', newline='', encoding=encoding) as f_in:
            lines = [line for line in f_in]

        # リストから1行文ずつデータを取り出し、検索ワードが含まれているかチェック
        for i in lines:
            if keyword in i:
                print(str(lines.index(i) + 1) + "行目でヒットしました")

    # キーワード検索
    def search_words_infiles(self, filepaths, keyword, ignore_exts=None):
        for filepath in filepaths:
            if os.path.isdir(filepath) == False:
                try:
                    self.search_words(filepath, keyword)
                except:
                    print("File Error:" + filepath)


def main():
    filedit = FilEdit()

    # 検索ワード
    keyword = "test"

    # 無視するファイル形式の拡張子
    ignore_exts = ["jpg", "png", "pdf"]

    # 検索対象のパス
    dir_path = "C:/github/sample/python/file"

    # 検索対象内の全てのファイル・フォルダパスを取得
    paths = filedit.get_paths(dir_path)

    # すべてのフォルダにあるファイルを対象に、中身に検索キーワードが含まれているかチェック
    filedit.search_words_infiles(paths["file_abs_path"], keyword,
                                 ignore_exts=ignore_exts)


"""
C:/github/sample/python/file\sample.txtをロードします
4行目でヒットしました
C:/github/sample/python/file\search_words.pyをロードします
4行目でヒットしました
24行目でヒットしました
C:/github/sample/python/file\search_words2.pyをロードします
32行目でヒットしました
C:/github/sample/python/file\sample\sample.txtをロードします
4行目でヒットしました
C:/github/sample/python/file\sample\a\sample.txtをロードします
4行目でヒットしました
"""

if __name__ == "__main__":
    main()
