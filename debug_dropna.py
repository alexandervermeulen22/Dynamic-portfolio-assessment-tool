import pandas as pd
import numpy as np
import utils.metrics as mt

# Simulate DataFrame with one good asset and one bad (all NaNs)
dates = pd.date_range(start='2023-01-01', periods=5)
df = pd.DataFrame({
    'AAPL': [100, 101, 102, 103, 104],
    'INVALID': [np.nan, np.nan, np.nan, np.nan, np.nan]
}, index=dates)

print("Original DF:\n", df)

# Logic in app.py currently:
# returns = mt.calculate_log_returns(df)
# In metrics.py: return np.log(prices / prices.shift(1)).dropna()

try:
    returns = mt.calculate_log_returns(df)
    print("Returns:\n", returns)
    if returns.empty:
        print("CRITICAL: Returns are empty because of one bad column!")
    else:
        print("Surprising success?")
        
except Exception as e:
    print(f"Error: {e}")
