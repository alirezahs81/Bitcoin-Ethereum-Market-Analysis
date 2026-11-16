import os
import pandas as pd
import yfinance as yf

# Directory used to store downloaded market data
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

SYMBOLS = {
    'BTC': 'BTC-USD',
    'ETH': 'ETH-USD'
}


def fetch_crypto_data(symbol_key='BTC', period='max', interval='1d'):
    """
    Download historical cryptocurrency market data from Yahoo Finance.

    Args:
        symbol_key: Cryptocurrency key ('BTC' or 'ETH').
        period: Historical data period (e.g. '1y', '2y', or 'max').
        interval: Data interval (e.g. '1d' or '1h').
    """
    if symbol_key not in SYMBOLS:
        raise ValueError(f"Invalid symbol. Allowed symbols: {list(SYMBOLS.keys())}")

    ticker = SYMBOLS[symbol_key]
    print(f"Downloading latest data for {symbol_key}...")

    # Use auto_adjust=True for consistent adjusted-price data across yfinance versions.
    df = yf.download(ticker, period=period, interval=interval, progress=False, auto_adjust=True)

    if df.empty:
        # Retry with the default download parameters.
        df = yf.download(ticker, period="2y", interval=interval, progress=False)

    if df.empty:
        raise Exception(f"Failed to download data for {symbol_key}")

    # Flatten multi-level columns returned by recent yfinance versions.
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)

    df = df.reset_index(drop=False)

    return df


def update_and_save_data(symbol_key='BTC'):
    """
    Download the latest available data and save it as a CSV file in the data directory.
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    file_path = os.path.join(DATA_DIR, f"{symbol_key}_data.csv")

    # Download the full available daily history.
    df = fetch_crypto_data(symbol_key=symbol_key, period='max', interval='1d')

    # Save the downloaded data to CSV.
    df.to_csv(file_path, index=False)
    print(f"Successfully saved {symbol_key} data to {file_path}.")
    return df


if __name__ == "__main__":
    # Run this module as a standalone data-download utility.
    for key in SYMBOLS.keys():
        update_and_save_data(key)
