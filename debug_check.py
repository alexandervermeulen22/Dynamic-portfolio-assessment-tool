import sys
print("Python executable:", sys.executable)

try:
    import streamlit
    print("Streamlit imported successfully")
except ImportError as e:
    print(f"Error importing Streamlit: {e}")

try:
    import pandas as pd
    import numpy as np
    print("Pandas/Numpy imported successfully")
except ImportError as e:
    print(f"Error importing Pandas/Numpy: {e}")

try:
    import yfinance as yf
    print("yfinance imported successfully")
except ImportError as e:
    print(f"Error importing yfinance: {e}")

try:
    import plotly
    print("Plotly imported successfully")
except ImportError as e:
    print(f"Error importing Plotly: {e}")

print("Checking local modules...")
try:
    import utils.data_loader as dl
    import utils.metrics as mt
    import utils.visualizations as vz
    print("Local modules imported successfully")
except Exception as e:
    print(f"Error importing local modules: {e}")
    import traceback
    traceback.print_exc()

# Test basic data fetch to see if yfinance works or errors (it requires internet)
print("Testing yfinance fetch...")
try:
    df = dl.fetch_historical_data(['FSR.JO'], '2023-01-01')
    print(f"Fetch result shape: {df.shape}")
    if df.empty:
        print("Warning: Fetch returned empty DataFrame")
except Exception as e:
    print(f"Error fetching data: {e}")
