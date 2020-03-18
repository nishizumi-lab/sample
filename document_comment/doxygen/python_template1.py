# -*- coding: utf-8 -*-
"""
@file ファイル名
@version バージョン番号
@author 作成者・更新者
@date パッケージの作成日時・更新日時
@brief 簡単な説明
@details 詳細な説明
@warning 警告メッセージ
@note メモ
"""

"""
@package パッケージの名前
@version バージョン番号
@author 作成者・更新者
@date 作成日時・更新日時
@brief 説明(簡単)
@details 説明（詳細）
@warning 警告メッセージ
@note メモ
"""

class MyClass(object):
    """
    @class クラス名
    @brief 説明(簡単)
    @details 説明（詳細）
    @warning 警告メッセージ
    @note メモ
    """

    def __init__(self,arg):
        """
        @fn __init__()
        @brief 説明(簡単) [例：クラスの初期化メソッド（コンストラクタ）]
        @param 引数の説明
        @return 戻り値の詳細（例：None 戻り値なし）
        @retval 戻り値の詳細：複数ある場合（例：sum_ab aとbの和（float））
        @retval 戻り値の詳細：複数ある場合（例：sub_ab aとbの差（float））
        @details 説明（詳細）
        @warning 警告メッセージ
        @note メモ
        """
        self.arg = arg

    def func(self,a:float,b:float) -> tuple:
        """
        @fn func()
        @brief 2つの値の和と差を計算します
        @param a 1つ目の値（float）
        @param b 2つ目の値（float)
        @retval sum_ab aとbの和（float）
        @retval sub_ab aとbの差（float）
        @details 詳細な説明
        @warning 警告メッセージ
        @note メモ
        """

        sum_ab = a+b
        sub_ab = a-b
        return sum_ab, sub_ab
