import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class GoldAnalyzer:
    def __init__(self, ticker="GC=F"):
        """
        初期化メソッド
        :param ticker: Yahoo Financeのティッカーシンボル (デフォルトはゴールド先物: GC=F)
        """
        self.ticker = ticker
        self.data = None

    def fetch_data(self, period="1y"):
        """
        データを取得する
        :param period: 取得期間 (例: '1y', '6mo', '1mo')
        """
        print(f"{self.ticker} のデータを取得中...")
        self.data = yf.download(self.ticker, period=period)
        if self.data.empty:
            print("データの取得に失敗しました。")
        else:
            print("データ取得完了。")
            # MultiIndexのカラムに対応する場合の処理 (yfinanceのバージョンによる)
            if isinstance(self.data.columns, pd.MultiIndex):
                 self.data.columns = self.data.columns.get_level_values(0)

    def fetch_data_multi_timeframe(self):
        """
        トップダウン分析用に日足と1時間足のデータを取得する
        """
        print(f"{self.ticker} のマルチタイムフレームデータを取得中...")
        
        # 日足 (長期トレンド判定用) - 過去1年
        self.daily_data = yf.download(self.ticker, period="1y", interval="1d")
        if isinstance(self.daily_data.columns, pd.MultiIndex):
             self.daily_data.columns = self.daily_data.columns.get_level_values(0)
             
        # 1時間足 (短期エントリー用) - 過去1ヶ月 (yfinanceの制限で長期間は取れない場合がある)
        self.hourly_data = yf.download(self.ticker, period="1mo", interval="1h")
        if isinstance(self.hourly_data.columns, pd.MultiIndex):
             self.hourly_data.columns = self.hourly_data.columns.get_level_values(0)

        if self.daily_data.empty or self.hourly_data.empty:
            print("マルチタイムフレームデータの取得に一部失敗しました。")
        else:
            print("マルチタイムフレームデータ取得完了。")

    def calculate_sma(self, window=20):
        """
        単純移動平均(SMA)を計算する
        :param window: 期間
        """
        if self.data is not None and not self.data.empty:
            column_name = f'SMA_{window}'
            self.data[column_name] = self.data['Close'].rolling(window=window).mean()
        else:
            print("データがありません。先にfetch_dataを実行してください。")

    def calculate_rsi(self, window=14):
        """
        RSI (Relative Strength Index) を計算する
        :param window: 期間
        """
        if self.data is not None and not self.data.empty:
            delta = self.data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

            rs = gain / loss
            self.data['RSI'] = 100 - (100 / (1 + rs))
        else:
            print("データがありません。先にfetch_dataを実行してください。")

    def analyze_entry_points(self):
        """
        エントリーポイントを分析する
        ゴールデンクロス/デッドクロス、RSIシグナルを判定
        """
        if self.data is None or self.data.empty:
             print("データがありません。")
             return

        self.data['Signal'] = 0
        
        # SMAクロス判定
        if 'SMA_20' in self.data.columns and 'SMA_50' in self.data.columns:
            # 前日と当日の値を取得してクロス判定
            prev_sma20 = self.data['SMA_20'].shift(1)
            prev_sma50 = self.data['SMA_50'].shift(1)
            
            # ゴールデンクロス: 前日SMA20 < 前日SMA50 AND 当日SMA20 > 当日SMA50
            golden_cross = (prev_sma20 < prev_sma50) & (self.data['SMA_20'] > self.data['SMA_50'])
            self.data.loc[golden_cross, 'Signal'] = 1
            
            # デッドクロス: 前日SMA20 > 前日SMA50 AND 当日SMA20 < 当日SMA50
            dead_cross = (prev_sma20 > prev_sma50) & (self.data['SMA_20'] < self.data['SMA_50'])
            self.data.loc[dead_cross, 'Signal'] = -1
            
        # RSIシグナル (既存のシグナルがない場合のみ追加)
        if 'RSI' in self.data.columns:
            # 売られすぎ (Buy)
            rsi_buy = (self.data['RSI'] < 30) & (self.data['Signal'] == 0)
            self.data.loc[rsi_buy, 'Signal'] = 1
            
            # 買われすぎ (Sell)
            rsi_sell = (self.data['RSI'] > 70) & (self.data['Signal'] == 0)
            self.data.loc[rsi_sell, 'Signal'] = -1

    def predict_future_trend(self, days=5):
        """
        線形回帰を用いて今後の価格トレンドを予測する
        :param days: 予測する日数
        """
        if self.data is None or self.data.empty:
            return

        # 直近30日分を使用
        recent_data = self.data['Close'].dropna().tail(30)
        
        if len(recent_data) < 2:
            print("予測に必要なデータが不足しています。")
            return

        y = recent_data.values
        x = np.arange(len(y))
        
        # 線形回帰 (1次関数)
        coef = np.polyfit(x, y, 1)
        poly1d_fn = np.poly1d(coef)
        
        # 将来のx値
        future_x = np.arange(len(y), len(y) + days)
        self.forecast_prices = poly1d_fn(future_x)
        
        # 日付の生成
        last_date = recent_data.index[-1]
        self.forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=days, freq='B')
        
        print(f"向こう{days}日間の予測価格: {self.forecast_prices}")

    def analyze_top_down(self):
        """
        トップダウン分析を実行する
        日足のトレンドと1時間足の状況を比較し、短期予測を行う
        """
        if not hasattr(self, 'daily_data') or not hasattr(self, 'hourly_data'):
            print("マルチタイムフレームデータがありません。fetch_data_multi_timeframeを実行してください。")
            return

        print("\n--- トップダウン分析結果 ---")

        # Step 1: 日足分析 (長期トレンド)
        self.daily_data['SMA_20'] = self.daily_data['Close'].rolling(window=20).mean()
        self.daily_data['SMA_50'] = self.daily_data['Close'].rolling(window=50).mean()
        
        current_daily_close = self.daily_data['Close'].iloc[-1]
        daily_sma20 = self.daily_data['SMA_20'].iloc[-1]
        daily_sma50 = self.daily_data['SMA_50'].iloc[-1]
        
        daily_trend = "レンジ/不明"
        if current_daily_close > daily_sma20 > daily_sma50:
            daily_trend = "上昇 (Uptrend)"
        elif current_daily_close < daily_sma20 < daily_sma50:
            daily_trend = "下降 (Downtrend)"
            
        print(f"【日足 (長期)】 トレンド: {daily_trend}")
        print(f"  現在値: {current_daily_close:.2f}, SMA20: {daily_sma20:.2f}, SMA50: {daily_sma50:.2f}")

        # Step 2: 1時間足分析 (短期状況)
        self.hourly_data['SMA_20'] = self.hourly_data['Close'].rolling(window=20).mean()
        self.hourly_data['SMA_50'] = self.hourly_data['Close'].rolling(window=50).mean()
        
        # RSI計算 (1時間足)
        delta = self.hourly_data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        self.hourly_data['RSI'] = 100 - (100 / (1 + rs))
        
        current_hourly_close = self.hourly_data['Close'].iloc[-1]
        hourly_rsi = self.hourly_data['RSI'].iloc[-1]
        hourly_sma20 = self.hourly_data['SMA_20'].iloc[-1]
        
        hourly_trend = "レンジ/不明"
        if current_hourly_close > hourly_sma20:
             hourly_trend = "短期上昇"
        elif current_hourly_close < hourly_sma20:
             hourly_trend = "短期下降"

        print(f"【1時間足 (短期)】 状態: {hourly_trend}, RSI: {hourly_rsi:.2f}")

        # Step 3: 総合判定 (シグナル)
        signal = "様子見 (Wait)"
        prediction = "明確な方向感が出るまで待機推奨。"
        
        if "上昇" in daily_trend and "短期上昇" in hourly_trend:
            if hourly_rsi < 70: # 買われすぎでなければ
                signal = "買い (STRONG BUY)"
                prediction = "長期・短期共に上昇トレンド。押し目買いの好機。直近高値を目指す展開を予想。"
            else:
                signal = "買い検討 (Wait for Dip)"
                prediction = "トレンドは強いが短期的に過熱感あり。少し調整が入ったところを狙いたい。"
                
        elif "下降" in daily_trend and "短期下降" in hourly_trend:
            if hourly_rsi > 30: # 売られすぎでなければ
                signal = "売り (STRONG SELL)"
                prediction = "長期・短期共に下降トレンド。戻り売り優勢。直近安値を更新する展開を予想。"
            else:
                signal = "売り検討 (Wait for Pullback)"
                prediction = "下落トレンド継続中だが、短期的に売られすぎ。一時的な反発に注意。"
        
        elif "上昇" in daily_trend and "短期下降" in hourly_trend:
             prediction = "長期的には上昇だが、短期的には調整局面。サポートラインでの反発を確認できれば買い。"
        
        elif "下降" in daily_trend and "短期上昇" in hourly_trend:
             prediction = "長期的には下降だが、短期的には反発局面。レジスタンスラインでの反落を確認できれば売り。"

        print(f"\n★ 判定シグナル: {signal}")
        print(f"★ 短期予測コメント: {prediction}")
        print("------------------------------------------\n")

    def analyze_top_down(self):
        """
        トップダウン分析を実行する
        日足のトレンドと1時間足の状況を比較し、短期予測を行う
        """
        if not hasattr(self, 'daily_data') or not hasattr(self, 'hourly_data'):
            print("マルチタイムフレームデータがありません。fetch_data_multi_timeframeを実行してください。")
            return

        print("\n--- トップダウン分析結果 (YouTube戦略ベース) ---")

        # Step 1: 日足分析 (長期トレンド)
        self.daily_data['SMA_20'] = self.daily_data['Close'].rolling(window=20).mean()
        self.daily_data['SMA_50'] = self.daily_data['Close'].rolling(window=50).mean()
        
        current_daily_close = self.daily_data['Close'].iloc[-1]
        daily_sma20 = self.daily_data['SMA_20'].iloc[-1]
        daily_sma50 = self.daily_data['SMA_50'].iloc[-1]
        
        daily_trend = "レンジ/不明"
        if current_daily_close > daily_sma20 > daily_sma50:
            daily_trend = "上昇 (Uptrend)"
        elif current_daily_close < daily_sma20 < daily_sma50:
            daily_trend = "下降 (Downtrend)"
            
        print(f"【日足 (長期)】 トレンド: {daily_trend}")
        print(f"  現在値: {current_daily_close:.2f}, SMA20: {daily_sma20:.2f}, SMA50: {daily_sma50:.2f}")

        # Step 2: 1時間足分析 (短期状況)
        self.hourly_data['SMA_20'] = self.hourly_data['Close'].rolling(window=20).mean()
        self.hourly_data['SMA_50'] = self.hourly_data['Close'].rolling(window=50).mean()
        
        # RSI計算 (1時間足)
        delta = self.hourly_data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        self.hourly_data['RSI'] = 100 - (100 / (1 + rs))
        
        current_hourly_close = self.hourly_data['Close'].iloc[-1]
        hourly_rsi = self.hourly_data['RSI'].iloc[-1]
        hourly_sma20 = self.hourly_data['SMA_20'].iloc[-1]
        
        hourly_trend = "レンジ/不明"
        if current_hourly_close > hourly_sma20:
             hourly_trend = "短期上昇"
        elif current_hourly_close < hourly_sma20:
             hourly_trend = "短期下降"

        print(f"【1時間足 (短期)】 状態: {hourly_trend}, RSI: {hourly_rsi:.2f}")

        # Step 3: 総合判定 (シグナル)
        signal = "様子見 (Wait)"
        prediction = "明確な方向感が出るまで待機推奨。"
        
        if "上昇" in daily_trend and "短期上昇" in hourly_trend:
            if hourly_rsi < 70: # 買われすぎでなければ
                signal = "買い (STRONG BUY)"
                prediction = "長期・短期共に上昇トレンド。押し目買いの好機。直近高値を目指す展開を予想。"
            else:
                signal = "買い検討 (Wait for Dip)"
                prediction = "トレンドは強いが短期的に過熱感あり。少し調整が入ったところを狙いたい。"
                
        elif "下降" in daily_trend and "短期下降" in hourly_trend:
            if hourly_rsi > 30: # 売られすぎでなければ
                signal = "売り (STRONG SELL)"
                prediction = "長期・短期共に下降トレンド。戻り売り優勢。直近安値を更新する展開を予想。"
            else:
                signal = "売り検討 (Wait for Pullback)"
                prediction = "下落トレンド継続中だが、短期的に売られすぎ。一時的な反発に注意。"
        
        elif "上昇" in daily_trend and "短期下降" in hourly_trend:
             prediction = "長期的には上昇だが、短期的には調整局面。サポートラインでの反発を確認できれば買い。"
        
        elif "下降" in daily_trend and "短期上昇" in hourly_trend:
             prediction = "長期的には下降だが、短期的には反発局面。レジスタンスラインでの反落を確認できれば売り。"

        print(f"\n★ 判定シグナル: {signal}")
        print(f"★ 短期予測コメント: {prediction}")
        print("------------------------------------------\n")

    def plot_data(self):
        """
        データをグラフ化する (価格とSMA, RSI)
        """
        if self.data is None or self.data.empty:
            print("データがありません。")
            return

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [3, 1]})

        # 価格とSMAのプロット
        ax1.plot(self.data.index, self.data['Close'], label='Close Price', alpha=0.5)
        
        # 計算済みのSMAをプロット
        for col in self.data.columns:
            if 'SMA' in col:
                ax1.plot(self.data.index, self.data[col], label=col)
        
        ax1.set_title(f'{self.ticker} Price Analysis')
        ax1.set_ylabel('Price (USD)')
        ax1.legend()
        ax1.grid(True)

        # 予測ラインのプロット
        if hasattr(self, 'forecast_dates') and hasattr(self, 'forecast_prices'):
             ax1.plot(self.forecast_dates, self.forecast_prices, label='Forecast', linestyle='--', color='orange', marker='o')

        # 売買シグナルのプロット
        if 'Signal' in self.data.columns:
            # Buy signal (Signal == 1)
            buy_signals = self.data[self.data['Signal'] == 1]
            ax1.scatter(buy_signals.index, buy_signals['Close'], marker='^', color='green', label='Buy Signal', s=100, zorder=5)
            
            # Sell signal (Signal == -1)
            sell_signals = self.data[self.data['Signal'] == -1]
            ax1.scatter(sell_signals.index, sell_signals['Close'], marker='v', color='red', label='Sell Signal', s=100, zorder=5)
            
            # 凡例を更新
            ax1.legend()

        # RSIのプロット
        if 'RSI' in self.data.columns:
            ax2.plot(self.data.index, self.data['RSI'], label='RSI', color='purple')
            ax2.axhline(70, linestyle='--', alpha=0.5, color='red')
            ax2.axhline(30, linestyle='--', alpha=0.5, color='green')
            ax2.set_title('Relative Strength Index (RSI)')
            ax2.set_ylabel('RSI')
            ax2.set_ylim(0, 100)
            ax2.legend()
            ax2.grid(True)

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    # テスト用
    analyzer = GoldAnalyzer()
    analyzer.fetch_data(period="6mo")
    analyzer.calculate_sma(20)
    analyzer.calculate_sma(50)
    analyzer.calculate_rsi()
    analyzer.plot_data()
