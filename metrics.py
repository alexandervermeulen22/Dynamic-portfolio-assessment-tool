import numpy as np
import pandas as pd

def calculate_log_returns(prices):
    """
    Calculates daily log returns from adjusted close prices.
    """
    return np.log(prices / prices.shift(1)).dropna()

def calculate_covariance_matrix(returns):
    """
    Calculates the covariance matrix of returns.
    """
    return returns.cov()

def calculate_portfolio_performance(weights, mean_returns, cov_matrix, risk_free_rate=0.0):
    """
    Calculates the expected annual return, annual volatility, and Sharpe ratio of the portfolio.
    Assumes 252 trading days.
    """
    weights = np.array(weights)
    returns = np.sum(mean_returns * weights) * 252
    volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix * 252, weights)))
    
    sharpe_ratio = 0
    if volatility > 0:
        sharpe_ratio = (returns - risk_free_rate) / volatility
        
    return returns, volatility, sharpe_ratio

def simulate_efficient_frontier(mean_returns, cov_matrix, num_portfolios=5000, risk_free_rate=0.0):
    """
    Simulates random portfolios to visualize the efficient frontier.
    Returns a DataFrame with returns, volatility, sharpe ratio, and weights.
    """
    results = np.zeros((3, num_portfolios))
    weights_record = []
    num_assets = len(mean_returns)
    
    for i in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        weights_record.append(weights)
        
        portfolio_return, portfolio_volatility, portfolio_sharpe = calculate_portfolio_performance(
            weights, mean_returns, cov_matrix, risk_free_rate
        )
        
        results[0,i] = portfolio_return
        results[1,i] = portfolio_volatility
        results[2,i] = portfolio_sharpe
        
    return results, weights_record

def calculate_beta(portfolio_returns, benchmark_returns):
    """
    Calculates the Beta of the portfolio relative to the benchmark.
    Beta = Cov(Portfolio, Benchmark) / Var(Benchmark)
    """
    # Align the series to ensure we are comparing same dates
    common_index = portfolio_returns.index.intersection(benchmark_returns.index)
    port_ret = portfolio_returns.loc[common_index]
    bench_ret = benchmark_returns.loc[common_index]
    
    # Covariance matrix between portfolio and benchmark
    # cov_matrix will be 2x2: [[Var(P), Cov(P,B)], [Cov(B,P), Var(B)]]
    matrix = np.cov(port_ret, bench_ret)
    beta = matrix[0, 1] / matrix[1, 1]
    
    beta = matrix[0, 1] / matrix[1, 1]
    
    return beta

def calculate_alpha(portfolio_return, benchmark_return, beta, risk_free_rate=0.0):
    """
    Calculates Jensen's Alpha.
    Alpha = R_p - [R_f + Beta * (R_m - R_f)]
    All inputs should be annualized.
    """
    expected_return = risk_free_rate + beta * (benchmark_return - risk_free_rate)
    alpha = portfolio_return - expected_return
    return alpha

def run_monte_carlo_simulation(weights, mean_returns, cov_matrix, years=5, num_simulations=1000, initial_investment=10000):
    """
    Runs a Monte Carlo simulation using Geometric Brownian Motion.
    Returns the simulation paths (DataFrame).
    """
    np.random.seed(42) # For reproducibility
    weights = np.array(weights)
    num_days = years * 252
    
    # Calculate portfolio mean and volatility
    port_return_daily = np.sum(mean_returns * weights)
    port_vol_daily = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    
    # Simulation
    # Formula: S_t = S_{t-1} * exp((mu - 0.5 * sigma^2) * dt + sigma * Z * sqrt(dt))
    # Here dt = 1 (daily steps implied by parameters)
    
    dt = 1
    
    simulation_data = np.zeros((num_days, num_simulations))
    simulation_data[0] = initial_investment
    
    for t in range(1, num_days):
        Z = np.random.normal(0, 1, num_simulations)
        drift = (port_return_daily - 0.5 * port_vol_daily**2) * dt
        shock = port_vol_daily * Z * np.sqrt(dt)
        
        simulation_data[t] = simulation_data[t-1] * np.exp(drift + shock)
        
    return pd.DataFrame(simulation_data)
