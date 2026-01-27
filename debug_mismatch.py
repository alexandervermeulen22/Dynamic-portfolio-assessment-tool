import utils.data_loader as dl
import utils.metrics as mt
import pandas as pd
import numpy as np

# Scenario: 3 tickers provided, but only 1 is valid (or logic failure)
# Or maybe the user entered 3 things that resulted in 1 valid ticker
tickers = ["AAPL", "INVALID1", "INVALID2"] 
print(f"Testing tickers: {tickers}")

try:
    df_prices = dl.fetch_historical_data(tickers, start_date='2023-01-01')
    print("Data fetched.")
    print("Columns:", df_prices.columns)
    print("Shape:", df_prices.shape)
    
    # App logic simulation
    num_assets = len(tickers) # 3
    weights = np.array([1/num_assets] * num_assets)
    print(f"Weights ({len(weights)}): {weights}")
    
    returns = mt.calculate_log_returns(df_prices)
    print("Returns calculated.")
    
    cov_matrix = mt.calculate_covariance_matrix(returns)
    print("Covariance calculated.")
    
    print("Attempting to calculate portfolio performance...")
    # This should crash
    port_return, port_vol, port_sharpe = mt.calculate_portfolio_performance(weights, returns.mean(), cov_matrix)
    print("Performance calculated (Unexpected):", port_return)

except Exception as e:
    print(f"CRASHED AS EXPECTED: {e}")
    # import traceback
    # traceback.print_exc()
