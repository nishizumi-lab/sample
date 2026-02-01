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
