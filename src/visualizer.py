import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_crypto_analysis(df, symbol_name="BTC"):
    """
    Create an advanced candlestick chart with moving averages, Bollinger Bands, and RSI.
    """
    if df.empty:
        raise ValueError("No data is available to plot.")

    # Ensure DataFrame columns are flat.
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)

    # Create two subplots: price and indicators on top, RSI below.
    fig = make_subplots(
        rows=2, cols=1,
        vertical_spacing=0.05,
        row_heights=[0.7, 0.3],
        subplot_titles=(f'{symbol_name} Price & Technical Indicators', 'Relative Strength Index (RSI)')
    )

    # 1. Price candlestick chart.
    fig.add_trace(
        go.Candlestick(
            x=df['Date'],
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Candlestick'
        ),
        row=1, col=1
    )

    # 2. 20-period Simple Moving Average.
    if 'SMA_20' in df.columns:
        fig.add_trace(
            go.Scatter(x=df['Date'], y=df['SMA_20'], line=dict(color='orange', width=1.5), name='SMA 20'),
            row=1, col=1
        )

    # 3. Bollinger Bands.
    if 'BB_Upper_20' in df.columns and 'BB_Lower_20' in df.columns:
        fig.add_trace(
            go.Scatter(x=df['Date'], y=df['BB_Upper_20'], line=dict(color='gray', width=1, dash='dash'), name='BB Upper'),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=df['Date'], y=df['BB_Lower_20'], line=dict(color='gray', width=1, dash='dash'), name='BB Lower', fill='tonexty', fillcolor='rgba(200,200,200,0.1)'),
            row=1, col=1
        )

    # 4. RSI indicator in the lower subplot.
    if 'RSI_14' in df.columns:
        fig.add_trace(
            go.Scatter(x=df['Date'], y=df['RSI_14'], line=dict(color='purple', width=1.5), name='RSI (14)'),
            row=2, col=1
        )
        # Reference lines for overbought (70) and oversold (30) levels.
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

    # Configure the chart layout with a dark theme.
    fig.update_layout(
        template='plotly_dark',
        title=f"<b>Comprehensive Market Analysis: {symbol_name}</b>",
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        xaxis_rangeslider_visible=False,
        height=800,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig


if __name__ == "__main__":
    from src.fetcher import update_and_save_data
    from src.indicators import add_all_indicators

    # Run a standalone visualization smoke test.
    df = update_and_save_data('BTC')
    df = add_all_indicators(df)

    fig = plot_crypto_analysis(df, "BTC")
    # Save the chart as an HTML file for inspection.
    fig.write_html("btc_analysis.html")
    print("Chart successfully generated and saved to btc_analysis.html.")
