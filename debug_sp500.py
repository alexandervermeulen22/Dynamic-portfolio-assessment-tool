import utils.data_loader as dl
import pandas as pd

# BRK.B is often tricky (BRK-B in yahoo, BRK.B elsewhere)
# BF.B is Brown-Forman
tickers = ["JPM", "PG", "BRK-B", "BRK.B", "BF-B", "SPY"]
print(f"Testing S&P 500 variants: {tickers}")

try:
    df = dl.fetch_historical_data(tickers, start_date='2023-01-01')
    print("Fetch completed.")
    print("Found columns:", df.columns.tolist())
    
    # Check which worked
    if 'BRK-B' in df.columns:
        print("BRK-B worked (Yahoo format)")
    elif 'BRK.B' in df.columns:
        print("BRK.B worked")
    else:
        print("WARNING: Berkshire Hathaway B failed")
        
except Exception as e:
    print(f"Error: {e}")
