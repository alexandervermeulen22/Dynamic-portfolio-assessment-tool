import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def plot_cumulative_returns(portfolio_cum_returns, benchmark_cum_returns=None, benchmark_name="Benchmark"):
    """
    Plots the cumulative returns of the portfolio and an optional benchmark.
    
    Args:
        portfolio_cum_returns (pd.Series): Cumulative returns of the portfolio.
        benchmark_cum_returns (pd.Series, optional): Cumulative returns of the benchmark.
        
    Returns:
        plotly.graph_objects.Figure
    """
    fig = go.Figure()
    
    # Convert to percentage return (Growth of $1 -> % Gain/Loss)
    portfolio_cum_returns = portfolio_cum_returns - 1
    
    # Portfolio Line
    fig.add_trace(go.Scatter(
        x=portfolio_cum_returns.index, 
        y=portfolio_cum_returns,
        mode='lines',
        name='Portfolio',
        line=dict(color='#1f77b4', width=3)
    ))
    
    # Benchmark Line
    if benchmark_cum_returns is not None:
        benchmark_cum_returns = benchmark_cum_returns - 1
        fig.add_trace(go.Scatter(
            x=benchmark_cum_returns.index, 
            y=benchmark_cum_returns,
            mode='lines',
            name=benchmark_name,
            line=dict(color='#ff7f0e', width=2, dash='dot')
        ))
        
    fig.update_layout(
        title='Cumulative Returns vs Benchmark',
        xaxis_title='Date',
        yaxis_title='Cumulative Return',
        template='plotly_white',
        hovermode="x unified",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        yaxis=dict(
            tickformat='.0%',  # Display as percentage
            dtick=0.10         # 10% increments
        )
    )
    
    return fig

def plot_correlation_heatmap(correlation_matrix):
    """
    Plots a heatmap of the correlation matrix.
    """
    fig = px.imshow(
        correlation_matrix, 
        text_auto=True, 
        aspect="auto",
        color_continuous_scale='RdBu_r',
        title="Asset Correlation Matrix"
    )
    return fig

import numpy as np

def plot_efficient_frontier_chart(results_array, current_portfolio=None):
    """
    Plots the efficient frontier simulation.
    results_array: [returns, volatilities, sharpe_ratios]
    current_portfolio: tuple (volatility, return) for the current portfolio marker
    """
    # Extract data for easier plotting
    returns = results_array[0]
    vols = results_array[1]
    sharpes = results_array[2]
    
    # Identify Max Sharpe Ratio Portfolio
    max_sharpe_idx = np.argmax(sharpes)
    max_sharpe_ret = returns[max_sharpe_idx]
    max_sharpe_vol = vols[max_sharpe_idx]
    
    fig = go.Figure()
    
    # 1. Simulation Points (Background)
    fig.add_trace(go.Scatter(
        x=vols,
        y=returns,
        mode='markers',
        marker=dict(
            color=sharpes,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Sharpe Ratio"),
            size=5
        ),
        name='Simulated Portfolios',
        text=[f"Sharpe: {s:.2f}" for s in sharpes],
        hoverinfo='text+x+y'
    ))
    
    # 2. Max Sharpe Ratio Portfolio (Gold Star)
    fig.add_trace(go.Scatter(
        x=[max_sharpe_vol],
        y=[max_sharpe_ret],
        mode='markers',
        marker=dict(
            size=20, 
            color='gold', 
            symbol='star', 
            line=dict(color='black', width=2)
        ),
        name='Max Sharpe Ratio'
    ))
    
    # 3. Current Portfolio (Red Star) - Added LAST to be on TOP
    if current_portfolio:
        port_vol, port_return = current_portfolio
        fig.add_trace(go.Scatter(
            x=[port_vol],
            y=[port_return],
            mode='markers',
            marker=dict(
                size=22, 
                color='#FF4B4B', 
                symbol='star', 
                line=dict(color='white', width=2)
            ),
            name='Current Portfolio'
        ))
        
    fig.update_layout(
        title='Efficient Frontier Simulation',
        xaxis_title='Volatility (Annualized)',
        yaxis_title='Return (Annualized)',
        template='plotly_white',
        hovermode='closest',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
        
    return fig

def plot_monte_carlo_simulation(simulation_df):
    """
    Plots the Monte Carlo simulation results with median and confidence intervals.
    """
    # Calculate percentiles
    median_path = simulation_df.median(axis=1)
    p05_path = simulation_df.quantile(0.05, axis=1)
    p95_path = simulation_df.quantile(0.95, axis=1)
    
    fig = go.Figure()
    
    # 5th Percentile (Lower Bound) - Hidden line for fill
    fig.add_trace(go.Scatter(
        x=simulation_df.index,
        y=p05_path,
        mode='lines',
        line=dict(width=0),
        showlegend=False,
        name='5th Percentile'
    ))
    
    # 95th Percentile (Upper Bound) - Fills to previous trace
    fig.add_trace(go.Scatter(
        x=simulation_df.index,
        y=p95_path,
        mode='lines',
        line=dict(width=0),
        fill='tonexty',
        fillcolor='rgba(0, 201, 255, 0.2)',
        name='95% Confidence Interval'
    ))
    
    # Median Path
    fig.add_trace(go.Scatter(
        x=simulation_df.index,
        y=median_path,
        mode='lines',
        line=dict(color='#00C9FF', width=3),
        name='Median Projection'
    ))
    
    fig.update_layout(
        title='Portfolio Forecast (Monte Carlo Simulation)',
        xaxis_title='Trading Days',
        yaxis_title='Portfolio Value',
        template='plotly_white',
        hovermode="x unified"
    )
    
    return fig
