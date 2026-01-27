import yfinance as yf
import pandas as pd
import numpy as np

def fetch_historical_data(tickers, start_date, end_date=None):
    """
    Fetches historical adjusted close prices for the given tickers.
    
    Args:
        tickers (list): List of ticker symbols (e.g., ['FSR.JO', 'NPN.JO']).
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str, optional): End date in 'YYYY-MM-DD' format.
        
    Returns:
        pd.DataFrame: DataFrame of Adjusted Close prices.
    """
    if not tickers:
        return pd.DataFrame()
    
    # yfinance expects a space-separated string or list
    data = yf.download(tickers, start=start_date, end=end_date, progress=False)
    
    if 'Adj Close' in data.columns:
        df = data['Adj Close']
    elif 'Close' in data.columns:
        df = data['Close']
    else:
        # Fallback if single ticker and structure is different
        df = data
        
    return df

def fetch_exchange_rates(start_date):
    """
    Fetches USD/ZAR exchange rate.
    """
    ticker = "USDZAR=X"
    data = yf.download(ticker, start=start_date, progress=False)
    if 'Adj Close' in data.columns:
        return data['Adj Close']
    return data['Close']

def get_esg_scores(tickers):
    """
    Generates mock ESG scores for the given tickers as a placeholder.
    In a real app, this would connect to an ESG data provider.
    """
    # Mock data: Random scores between 0 and 100, correlated slightly with "tech" or "green" names if we were fancy
    # For now, just random reproducible scores
    np.random.seed(42)
    scores = {}
    for t in tickers:
        scores[t] = np.random.randint(50, 95)
    
    return pd.DataFrame(list(scores.items()), columns=['Ticker', 'ESG Score'])
