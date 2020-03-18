from filedit.file_searcher import FileSearcher

fsearch = FileSearcher()

# 検索ワード
KEYWORDS = ["test", "tes"]

# 無視するファイル形式の拡張子
IGNORE_EXTS = [".jpg", ".png", ".pdf", ".vs", ".py"]

# 検索対象のパス
LOAD_DIR_PATH = "C:/github/sample/python/file"

# 検索結果の出力先
SAVE_FILE_PATH = "C:/github/sample/python/file/result.csv"

# 検索対象内の全てのファイル・フォルダパスを取得
paths = fsearch.get_paths(LOAD_DIR_PATH)

# すべてのフォルダにあるファイルを対象に、中身に検索キーワードが含まれているかチェック
result = fsearch.search_words_infiles(paths["file_abs_path"], keywords=KEYWORDS,
                                         ignore_exts=IGNORE_EXTS)

fsearch.save_result(SAVE_FILE_PATH, result)

"""
Console outputs
------------------------
Load：C:/github/sample/python/file\sample\sample.txt
index:4, word:test
index:4, word:tes
------------------------
Load：C:/github/sample/python/file\sample\a\sample.txt
index:4, word:test
index:4, word:tes
"""

"""
result.csv

3,test,C:/github/sample/python/file\sample.txt
3,tes,C:/github/sample/python/file\sample.txt
3,test,C:/github/sample/python/file\sample\sample.txt
3,tes,C:/github/sample/python/file\sample\sample.txt
3,test,C:/github/sample/python/file\sample\a\sample.txt
3,tes,C:/github/sample/python/file\sample\a\sample.txt
"""

