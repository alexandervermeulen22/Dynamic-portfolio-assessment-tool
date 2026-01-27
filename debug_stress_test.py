import utils.data_loader as dl
import utils.metrics as mt
import pandas as pd
import numpy as np
import time

# Generate/Use a list of 100 tickers (Subset of NASDAQ/S&P)
# For the sake of the script, I'll use a hardcoded list of major tech and S&P companies
# If I need exactly 100, I can use a comprehensive list or repeat some if just testing load (though repeating breaks cov matrix potentially due to perfect correlation singular matrix issues? No, cov handles it, but let's try distinct ones)

tickers = [
    "AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "META", "TSLA", "PEP", "AVGO", "CSCO",
    "TMUS", "CMCSA", "ADBE", "NFLX", "TXN", "PYPL", "AMD", "QCOM", "INTC", "HON",
    "INTU", "AMGN", "COST", "SBUX", "MDLZ", "GILD", "ISRG", "BKNG", "ADI", "VRTX",
    "REGN", "LRCX", "FISV", "ATVI", "CSX", "KLAC", "ILMN", "PANW", "SNPS", "CDNS",
    "AEP", "MAR", "NXPI", "DXCM", "MELI", "KDP", "MNST", "ORLY", "CTAS", "PCAR",
    "EXC", "LULU", "ADSK", "XEL", "IDXX", "PAYX", "ROST", "MRVL", "EA", "WDAY",
    "CTSH", "VRSK", "SGEN", "ODFL", "BIIB", "MCHP", "DLTR", "CPRT", "FAST", "WBA",
    "ANSS", "SIRI", "EBAY", "TEAM", "VRSN", "SWKS", "ZS", "ALGN", "CDW", "LCID", 
    "ZM", "JD", "DDOG", "RIVN", "PDD", "OKTA", "CRWD", "DOCU", "SPLK", "MTCH",
    "NTES", "CHKP", "SWAV", "ENPH", "ASML", "AZN", "BKR", "GFS", "KHC", "MRNA"
]

print(f"Testing with {len(tickers)} tickers...")
start_time = time.time()

try:
    df_prices = dl.fetch_historical_data(tickers, start_date='2023-01-01')
    print(f"Fetch completed in {time.time() - start_time:.2f} seconds.")
    print("Shape:", df_prices.shape)
    
    if df_prices.shape[1] < 50:
        print("WARNING: Seems many tickers failed to download?")
        
    print("Calculating metrics...")
    returns = mt.calculate_log_returns(df_prices)
    cov = mt.calculate_covariance_matrix(returns)
    
    weights = np.array([1/len(df_prices.columns)] * len(df_prices.columns))
    
    perf = mt.calculate_portfolio_performance(weights, returns.mean(), cov)
    print("Performance calculated:", perf)
    
    print("Attempting Efficient Frontier Simulation (heavy compute)...")
    sim_start = time.time()
    mt.simulate_efficient_frontier(returns.mean(), cov, num_portfolios=1000) # Reduced to 1000 for quick test
    print(f"Simulation completed in {time.time() - sim_start:.2f} seconds.")
    
    print("SUCCESS: 100-ticker load test passed.")

except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()
