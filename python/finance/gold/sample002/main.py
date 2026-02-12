from gold_analyzer import GoldAnalyzer
import sys

def main():
    print("ゴールド価格分析ツールを開始します...")

    # デフォルト設定
    ticker = "GC=F" # ゴールド先物
    period = "1y"   # 過去1年分

    # インスタンス作成
    analyzer = GoldAnalyzer(ticker=ticker)

    # データ取得
    analyzer.fetch_data(period=period)

    # データが取得できた場合のみ分析・可視化
    if analyzer.data is not None and not analyzer.data.empty:
        # テクニカル指標計算
        analyzer.calculate_sma(window=20) # 20日移動平均
        analyzer.calculate_sma(window=50) # 50日移動平均
        analyzer.calculate_rsi(window=14) # RSI

        # エントリーポイント分析
        analyzer.analyze_entry_points()

        # 今後のトレンド予測 (5日間)
        analyzer.predict_future_trend(days=5)

        # トップダウン分析
        analyzer.fetch_data_multi_timeframe()
        analyzer.analyze_top_down()

        # グラフ表示
        print(f"{ticker} の分析結果を表示します。ウィンドウを閉じて終了してください。")
        analyzer.plot_data()
    else:
        print("データ取得に失敗したため、終了します。")

if __name__ == "__main__":
    main()
