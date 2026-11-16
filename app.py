import streamlit as st
import pandas as pd
import os

from src.fetcher import update_and_save_data, SYMBOLS
from src.indicators import add_all_indicators
from src.visualizer import plot_crypto_analysis

# Configure the Streamlit page
st.set_page_config(
    page_title="Crypto Market Analysis Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("🚀 Cryptocurrency Market Analysis Dashboard")
st.markdown("Comprehensive Bitcoin and Ethereum market analysis with advanced technical indicators")

# Sidebar controls
st.sidebar.header("Dashboard Settings")

selected_symbol = st.sidebar.selectbox(
    "Select Cryptocurrency:",
    options=list(SYMBOLS.keys()),
    format_func=lambda x: "Bitcoin (BTC)" if x == "BTC" else "Ethereum (ETH)"
)

if st.sidebar.button("🔄 Update Live Market Data"):
    with st.spinner("Fetching the latest market data..."):
        try:
            update_and_save_data(selected_symbol)
            st.sidebar.success("Data successfully updated!")
        except Exception as e:
            st.sidebar.error(f"Update failed: {e}")

# Load market data
data_path = os.path.join(os.path.dirname(__file__), 'data', f"{selected_symbol}_data.csv")

if not os.path.exists(data_path):
    with st.spinner(f"No data found. Fetching initial {selected_symbol} data..."):
        try:
            update_and_save_data(selected_symbol)
        except Exception as e:
            st.error(f"Data download failed: {e}")

if os.path.exists(data_path):
    df = pd.read_csv(data_path)

    # Calculate technical indicators
    df = add_all_indicators(df)

    # Display key metrics at the top of the dashboard
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    price_change = latest['Close'] - prev['Close']
    price_change_pct = (price_change / prev['Close']) * 100

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Latest Price (USD)", f"${latest['Close']:,.2f}", f"{price_change_pct:.2f}%")
    col2.metric("Daily High", f"${latest['High']:,.2f}")
    col3.metric("Daily Low", f"${latest['Low']:,.2f}")
    col4.metric("RSI (14)", f"{latest.get('RSI_14', 0):.2f}")

    st.markdown("---")

    # Select the chart time range
    timeframe = st.sidebar.radio(
        "Chart Time Range:",
        options=['1 Month', '3 Months', '6 Months', '1 Year', 'All History'],
        index=3
    )

    filtered_df = df.copy()
    filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])

    if timeframe == '1 Month':
        filtered_df = filtered_df.tail(30)
    elif timeframe == '3 Months':
        filtered_df = filtered_df.tail(90)
    elif timeframe == '6 Months':
        filtered_df = filtered_df.tail(180)
    elif timeframe == '1 Year':
        filtered_df = filtered_df.tail(365)

    # Render the Plotly chart
    fig = plot_crypto_analysis(filtered_df, selected_symbol)
    st.plotly_chart(fig, use_container_width=True)

    # Display recent market data
    with st.expander("📁 View Raw Data and Technical Indicators"):
        st.dataframe(df.tail(50).sort_index(ascending=False))

else:
    st.warning("Please fetch the data for the selected cryptocurrency first.")
