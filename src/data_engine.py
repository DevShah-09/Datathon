import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import logging
import os

# Redirect yfinance cache to avoid permissions/WinError 183
cache_dir = os.path.join(os.getcwd(), ".cache", "yfinance")
os.makedirs(cache_dir, exist_ok=True)
yf.set_tz_cache_location(cache_dir)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataEngine:
    def __init__(self, tickers=None):
        if tickers is None:
            # Default set of major banks and tech for simulation
            self.tickers = [
                'JPM', 'GS', 'MS', 'BAC', 'C',  # Big Hubs
                'WFC', 'HSBC', 'UBS', 'DB', 'BNP.PA', # Major Spoke/Hubs (Added BNP, removed CS)
                'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', # Tech for market sentiment
                'V', 'MA', 'AXP', 'PYPL', 'BLK'  # Financial services
            ]
        else:
            self.tickers = tickers

    def get_historical_data(self, period="1y", interval="1d"):
        """
        Pulls daily adjusted prices and volume.
        auto_adjust=True handles stock splits automatically.
        """
        logger.info(f"Fetching historical data for {len(self.tickers)} tickers...")
        data = yf.download(
            self.tickers, 
            period=period, 
            interval=interval, 
            group_by='ticker', 
            auto_adjust=True
        )
        return data

    def get_latest_metrics(self, data):
        """
        Calculates rolling volatility and returns the latest price/vol for each ticker.
        """
        metrics = {}
        for ticker in self.tickers:
            try:
                # Get close prices for this ticker
                if isinstance(data.columns, pd.MultiIndex):
                    ticker_data = data[ticker]
                else:
                    ticker_data = data
                
                close = ticker_data['Close']
                returns = close.pct_change()
                volatility = returns.rolling(window=30).std() * (252**0.5) # Annualized
                
                metrics[ticker] = {
                    'price': close.iloc[-1],
                    'volatility': volatility.iloc[-1],
                    'prev_price': close.iloc[-2] if len(close) > 1 else close.iloc[-1]
                }
            except Exception as e:
                logger.error(f"Error processing {ticker}: {e}")
        return metrics

if __name__ == "__main__":
    engine = DataEngine()
    hist_data = engine.get_historical_data(period="1mo")
    latest = engine.get_latest_metrics(hist_data)
    print(pd.DataFrame(latest).T)
