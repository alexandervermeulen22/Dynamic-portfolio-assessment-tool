import utils.data_loader as dl
import utils.metrics as mt
import pandas as pd
import numpy as np

tickers = ["AAPL", "MSFT", "AMZN", "NVDA", "GOOGL"]
benchmark = "QQQ"
print(f"Fetching data for: {tickers} using yfinance...")

try:
    df_prices = dl.fetch_historical_data(tickers, start_date='2023-01-01')
    print("Data fetched.")
    print("Columns:", df_prices.columns)
    print("Head:\n", df_prices.head())
    
    # Check structure - yfinance changed recently to return MultiIndex columns [('Adj Close', 'AAPL'), ...] sometimes?
    # Or simply AAPL, MSFT, etc.
    
    if df_prices.empty:
        print("ERROR: DataFrame is empty.")
    else:
        print("Detailed verification...")
        print("Data Types:\n", df_prices.dtypes)
        
        print("Fetching Benchmark...")
        df_benchmark = dl.fetch_historical_data([benchmark], start_date='2023-01-01')
        print("Benchmark Head:\n", df_benchmark.head())
        
        # Simulating App Logic
        common_index = df_prices.index.intersection(df_benchmark.index)
        df_prices = df_prices.loc[common_index]
        df_benchmark = df_benchmark.loc[common_index]
        
        print(f"Index intersection size: {len(common_index)}")
        
        returns = mt.calculate_log_returns(df_prices)
        print("Returns calculated.")
        print(returns.head())
        
        # Check for NaN/Inf
        if returns.isnull().values.any():
            print("WARNING: Returns contain NaNs")
        if np.isinf(returns.values).any():
            print("WARNING: Returns contain Infs")
            
        print("Calculating covariance...")
        cov = mt.calculate_covariance_matrix(returns)
        print("Covariance calculated.")
        
        weights = np.array([1/len(tickers)] * len(tickers))
        perf = mt.calculate_portfolio_performance(weights, returns.mean(), cov)
        print("Performance:", perf)

except Exception as e:
    print("CRASHED:")
    print(e)
    import traceback
    traceback.print_exc()
