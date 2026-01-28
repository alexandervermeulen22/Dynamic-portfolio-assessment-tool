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

def plot_efficient_frontier_chart(results_array, portfolio_vol=None, portfolio_return=None):
    """
    Plots the efficient frontier simulation and optionally highlights the current portfolio.
    results_array: [returns, volatilities, sharpe_ratios]
    portfolio_vol: float, optional - Current portfolio volatility
    portfolio_return: float, optional - Current portfolio return
    """
    df = pd.DataFrame({
        'Return': results_array[0],
        'Volatility': results_array[1],
        'Sharpe': results_array[2]
    })
    
    fig = px.scatter(
        df, x='Volatility', y='Return', color='Sharpe',
        color_continuous_scale='Viridis',
        title='Efficient Frontier Simulation',
        labels={'Sharpe': 'Sharpe Ratio'}
    )

    # Add Current Portfolio Marker
    if portfolio_vol is not None and portfolio_return is not None:
        fig.add_trace(go.Scatter(
            x=[portfolio_vol],
            y=[portfolio_return],
            mode='markers',
            marker=dict(
                color='red', 
                size=18, 
                symbol='star',
                line=dict(width=2, color='white') # White border for contrast
            ),
            name='Current Portfolio'
        ))

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
