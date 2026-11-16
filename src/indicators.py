import pandas as pd
import numpy as np


def calculate_sma(df, window=20, price_col='Close'):
    """Calculate the Simple Moving Average (SMA)."""
    df[f'SMA_{window}'] = df[price_col].rolling(window=window).mean()
    return df


def calculate_ema(df, window=20, price_col='Close'):
    """Calculate the Exponential Moving Average (EMA)."""
    df[f'EMA_{window}'] = df[price_col].ewm(span=window, adjust=False).mean()
    return df


def calculate_rsi(df, window=14, price_col='Close'):
    """Calculate the Relative Strength Index (RSI)."""
    delta = df[price_col].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    rs = gain / loss
    df[f'RSI_{window}'] = 100 - (100 / (1 + rs))
    return df


def calculate_bollinger_bands(df, window=20, num_std=2, price_col='Close'):
    """Calculate Bollinger Bands."""
    sma = df[price_col].rolling(window=window).mean()
    std = df[price_col].rolling(window=window).std()

    df[f'BB_Middle_{window}'] = sma
    df[f'BB_Upper_{window}'] = sma + (std * num_std)
    df[f'BB_Lower_{window}'] = sma - (std * num_std)
    return df


def add_all_indicators(df):
    """Add all supported technical indicators to the DataFrame."""
    if df.empty:
        return df

    # Copy the DataFrame to avoid SettingWithCopyWarning.
    df = df.copy()

    # Flatten MultiIndex columns when present.
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)

    # Validate the Close column and convert it to numeric values.
    if 'Close' in df.columns:
        df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    else:
        raise KeyError("The 'Close' column was not found in the data.")

    # Calculate technical indicators.
    df = calculate_sma(df, window=20)
    df = calculate_sma(df, window=50)
    df = calculate_ema(df, window=20)
    df = calculate_rsi(df, window=14)
    df = calculate_bollinger_bands(df, window=20)

    # Calculate daily percentage returns.
    df['Daily_Return'] = df['Close'].pct_change() * 100

    return df


if __name__ == "__main__":
    # Test the indicator module using locally stored Bitcoin data.
    import os
    from src.fetcher import update_and_save_data

    btc_df = update_and_save_data('BTC')
    btc_processed = add_all_indicators(btc_df)
    print("Sample of processed data with technical indicators:")
    if isinstance(btc_processed.columns, pd.MultiIndex):
        btc_processed.columns = btc_processed.columns.droplevel(0)
    print(btc_processed[['Date', 'Close', 'SMA_20', 'RSI_14', 'Daily_Return']].tail(5))
