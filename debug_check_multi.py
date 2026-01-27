import utils.data_loader as dl
import utils.metrics as mt
import pandas as pd
import numpy as np

tickers = ["FSR.JO", "NPN.JO", "SBK.JO", "CPI.JO"]
print(f"Fetching data for: {tickers}")

try:
    df_prices = dl.fetch_historical_data(tickers, start_date='2023-01-01')
    print("Data fetched.")
    print("Columns:", df_prices.columns)
    print("Head:\n", df_prices.head())
    
    if df_prices.empty:
        print("ERROR: DataFrame is empty.")
    else:
        print("Calculating returns...")
        returns = mt.calculate_log_returns(df_prices)
        print("Returns calculated.")
        print("Returns Head:\n", returns.head())
        
        print("Calculating covariance...")
        cov = mt.calculate_covariance_matrix(returns)
        print("Covariance matrix shape:", cov.shape)
        
        weights = np.array([0.25, 0.25, 0.25, 0.25])
        print("Calculating performance...")
        perf = mt.calculate_portfolio_performance(weights, returns.mean(), cov)
        print("Performance:", perf)
        
        print("ALL CHECKS PASSED.")

except Exception as e:
    print("CRASHED:")
    print(e)
    import traceback
    traceback.print_exc()
