import yfinance as yf
import pandas as pd

# subset of tickers including some known to work and some likely to fail
tickers = ["AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "INTC", "AMD", "CSCO"]
print("Downloading...")
data = yf.download(tickers, start="2023-01-01", progress=False)
print("Raw Data Columns:", data.columns)
print("Raw Data Head:\n", data.head())

if 'Adj Close' in data.columns:
    print("Adj Close slice:\n", data['Adj Close'].head())
    
# Check what happens if we mix in a bad one
tickers_mixed = ["AAPL", "INVALID_XYZ"]
data_mixed = yf.download(tickers_mixed, start="2023-01-01", progress=False)
print("Mixed Columns:", data_mixed.columns)
