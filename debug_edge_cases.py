import utils.data_loader as dl
import pandas as pd

# Test case 1: Trailing comma resulting in empty string
tickers = ["AAPL", "MSFT", ""]
print(f"Testing tickers: {tickers}")

try:
    df = dl.fetch_historical_data(tickers, start_date='2023-01-01')
    print("Success with empty string.")
    print(df.head())
except Exception as e:
    print(f"Failed with empty string: {e}")

# Test case 2: Invalid ticker
tickers = ["AAPL", "INVALID_TICKER_XYZ"]
print(f"Testing tickers: {tickers}")
try:
    df = dl.fetch_historical_data(tickers, start_date='2023-01-01')
    print("Success with invalid ticker.")
    print("Columns:", df.columns)
    # yfinance usually drops invalid tickers but might print error
except Exception as e:
    print(f"Failed with invalid ticker: {e}")
