import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Ensure the root directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Robust Import Strategy: Try importing from 'utils' first (local structure),
# then fall back to root imports (server structure appears flat)
try:
    import utils.data_loader as dl
    import utils.metrics as mt
    import utils.visualizations as vz
except ImportError:
    # If utils folder doesn't exist or isn't a package, try direct imports
    import data_loader as dl
    import metrics as mt
    import visualizations as vz

# Page Config
st.set_page_config(
    page_title="Dynamic Portfolio Assessment",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Premium" feel
st.markdown("""
<style>
    .metric-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    h1 {
        background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stButton>button {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        color: black;
        border: none;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Title using the gradient style
st.title("Dynamic Portfolio Assessment Tool")

# Sidebar
st.sidebar.header("Portfolio Configuration")

# Ticker Input
default_tickers = "AAPL, MSFT, AMZN, NVDA, GOOGL"
tickers_input = st.sidebar.text_area("Enter Tickers (comma separated)", value=default_tickers, help="Supports NASDAQ 100, S&P 500, and global tickers. For stocks like Berkshire Hathaway, use 'BRK-B' instead of 'BRK.B'.")
tickers = [t.strip() for t in tickers_input.split(',') if t.strip()]

# Date Range
col1, col2 = st.sidebar.columns(2)
start_date = col1.date_input("Start Date", value=datetime(2023, 1, 1))
end_date = col2.date_input("End Date", value=datetime.today())

# Risk Free Rate
rf_rate = st.sidebar.number_input("Risk Free Rate (%)", value=4.5, step=0.1) / 100

# Benchmark (Proxy)
benchmark_ticker = st.sidebar.text_input("Benchmark Ticker", value="QQQ")

# Asset Allocation
with st.sidebar.expander("Customize Weights"):
    st.caption("Default: Equal Weights. Enter relative values (e.g. 50, 30, 20). Weights will be normalized automatically.")
    input_weights = {}
    for t in tickers:
        input_weights[t] = st.number_input(f"Weight for {t}", min_value=0.0, value=1.0, step=0.5, key=f"w_{t}")

# Analyze Button Logic
if st.sidebar.button("Analyze Portfolio"):
    # Security: Limit number of tickers to prevent resource exhaustion
    if len(tickers) > 50:
        st.error("Too many tickers selected. Please limit to 50 or fewer to ensure stability.")
    else:
        st.session_state['analyzed'] = True

if st.session_state.get('analyzed', False):
    try:
        with st.spinner("Fetching Market Data..."):
            # 1. Fetch Data
            df_prices = dl.fetch_historical_data(tickers, start_date=start_date, end_date=end_date)
            df_benchmark = dl.fetch_historical_data([benchmark_ticker], start_date=start_date, end_date=end_date)
            
            if df_prices.empty:
                st.error("No data found for the specified tickers. Please checks the tickers and date range.")
            else:
                # Align dates
                common_index = df_prices.index.intersection(df_benchmark.index)
                df_prices = df_prices.loc[common_index]
                df_benchmark = df_benchmark.loc[common_index]
                
                # Drop tickers that failed to fetch (all NaNs)
                df_prices.dropna(axis=1, how='all', inplace=True)
                
                # Update tickers list to match what was actually fetched
                tickers = df_prices.columns.tolist()
                
                if not tickers:
                    st.error("All selected tickers failed to fetch data.")
                    st.stop()
                
                # Calculate Weights
                # Filter input weights for only the VALID tickers that were fetched
                valid_weights = [input_weights.get(t, 1.0) for t in tickers]
                weights = np.array(valid_weights)
                
                # Normalize
                if weights.sum() == 0:
                     weights = np.array([1/len(tickers)] * len(tickers)) # Fallback to equal if all zeros
                else:
                     weights = weights / weights.sum()
                
                # 2. Risk Metrics
                returns = mt.calculate_log_returns(df_prices)
                benchmark_returns = mt.calculate_log_returns(df_benchmark)
                
                # Handle Single Ticker Benchmark
                if isinstance(benchmark_returns, pd.DataFrame):
                    benchmark_returns = benchmark_returns.iloc[:, 0]
                
                cov_matrix = mt.calculate_covariance_matrix(returns)
                port_return, port_vol, port_sharpe = mt.calculate_portfolio_performance(weights, returns.mean(), cov_matrix, risk_free_rate=rf_rate)
                
                # Calculate Portfolio Daily Returns for Beta calculation
                # (Weighted sum of asset returns)
                port_daily_returns = returns.dot(weights)
                
                # Calculate Beta
                beta = mt.calculate_beta(port_daily_returns, benchmark_returns)
                
                # Calculate Alpha
                # We need annualized benchmark return just like portfolio return
                bench_annual_return = benchmark_returns.mean() * 252
                alpha = mt.calculate_alpha(port_return, bench_annual_return, beta, risk_free_rate=rf_rate)
                
                # 3. Display Top Metrics
                st.markdown("---")
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Expected Annual Return", f"{port_return:.2%}", delta_color="normal")
                m2.metric("Portfolio Beta", f"{beta:.2f}", delta_color="off")
                m3.metric("Jensen's Alpha", f"{alpha:.2%}", delta_color="normal")
                m4.metric("Sharpe Ratio", f"{port_sharpe:.2f}")
                
                # 4. Charts
                st.markdown("### Performance & Analysis")
                
                # Cumulative Returns
                port_cum_returns = (1 + returns).cumprod()
                # Simplified: Cumulative return of the portfolio value
                # Portfolio Daily Returns = weighted sum of asset daily returns
                port_daily_returns = returns.dot(weights)
                port_cum_ret_series = (1 + port_daily_returns).cumprod()
                
                bench_cum_ret_series = (1 + benchmark_returns).cumprod()
                
                fig_cum = vz.plot_cumulative_returns(port_cum_ret_series, bench_cum_ret_series, benchmark_name=benchmark_ticker)
                st.plotly_chart(fig_cum, use_container_width=True)
                
                col_chart1, col_chart2 = st.columns(2)
                
                with col_chart1:
                    st.subheader("Asset Correlations")
                    fig_corr = vz.plot_correlation_heatmap(returns.corr())
                    st.plotly_chart(fig_corr, use_container_width=True)
                    
                with col_chart2:
                    st.subheader("Efficient Frontier Simulation")
                    sim_res, _ = mt.simulate_efficient_frontier(returns.mean(), cov_matrix, risk_free_rate=rf_rate)
                    fig_ef = vz.plot_efficient_frontier_chart(sim_res, portfolio_vol=port_vol, portfolio_return=port_return)
                    # Add current portfolio marker (Now handled inside the function)
                    st.plotly_chart(fig_ef, use_container_width=True)

                # 5. ESG & Data
                st.markdown("### ESG & Holdings Data")
                esg_df = dl.get_esg_scores(tickers)
                esg_df['Weight'] = [f"{w:.1%}" for w in weights]
                esg_df.index = range(1, len(esg_df) + 1)
                st.dataframe(esg_df, use_container_width=True)
                
                # 6. Monte Carlo Simulation (Predictive Model)
                st.markdown("---")
                st.markdown("### Future Performance Forecast (Monte Carlo)")
                
                with st.expander("Forecast Settings", expanded=True):
                    sim_years = st.slider("Forecast Horizon (Years)", 1, 10, 5)
                    initial_inv = st.number_input("Initial Investment ($)", value=10000, step=1000)
                    
                    if st.button("Run Simulation"):
                        with st.spinner("Running 1,000 simulations..."):
                             sim_results = mt.run_monte_carlo_simulation(weights, returns.mean(), cov_matrix, years=sim_years, initial_investment=initial_inv)
                             
                             # Plot
                             fig_mc = vz.plot_monte_carlo_simulation(sim_results)
                             st.plotly_chart(fig_mc, use_container_width=True)
                             
                             # Stats
                             final_values = sim_results.iloc[-1]
                             median_val = final_values.median()
                             p95_val = final_values.quantile(0.95)
                             p05_val = final_values.quantile(0.05)
                             
                             c1, c2, c3 = st.columns(3)
                             c1.metric(f"Median Value ({sim_years}y)", f"${median_val:,.2f}")
                             c2.metric("Optimistic (95%)", f"${p95_val:,.2f}")
                             c3.metric("Pessimistic (5%)", f"${p05_val:,.2f}")

                # Export
                st.download_button("Download Price Data", df_prices.to_csv(), "price_data.csv")
    except Exception as e:
        # Security: Do not expose raw exception details to user (info leakage)
        st.error("An error occurred during analysis. Please check your inputs and try again.")
        # Log the actual error for debugging (in a real app this would go to a log file)
        print(f"Error: {e}")

else:
    st.info("👈 Enter tickers in the sidebar and click 'Analyze Portfolio' to start.")

