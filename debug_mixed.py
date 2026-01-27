import utils.data_loader as dl
import pandas as pd

# NASDAQ 100: AAPL, MSFT, NVDA
# S&P 500 (Non-Tech/Non-NASDAQ): JPM (Bank), JNJ (Pharma), XOM (Energy), PG (Consumer)
mix_tickers = ["AAPL", "MSFT", "NVDA", "JPM", "JNJ", "XOM", "PG"]
print(f"Testing mixed indices: {mix_tickers}")

try:
    df = dl.fetch_historical_data(mix_tickers, start_date='2023-01-01')
    print("Fetch successfully.")
    print("Columns obtained:", df.columns.tolist())
    
    missing = set(mix_tickers) - set(df.columns)
    if missing:
        print(f"FAILED: Missing tickers: {missing}")
    else:
        print("SUCCESS: All mixed tickers found.")
        
except Exception as e:
    print(f"CRITICAL FAIL: {e}")
