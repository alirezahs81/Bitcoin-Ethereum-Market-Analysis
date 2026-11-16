import pandas as pd
import numpy as np

def calculate_sma(df, window=20, price_col='Close'):
    """محاسبه میانگین متحرک ساده (Simple Moving Average)"""
    df[f'SMA_{window}'] = df[price_col].rolling(window=window).mean()
    return df

def calculate_ema(df, window=20, price_col='Close'):
    """محاسبه میانگین متحرک نمایی (Exponential Moving Average)"""
    df[f'EMA_{window}'] = df[price_col].ewm(span=window, adjust=False).mean()
    return df

def calculate_rsi(df, window=14, price_col='Close'):
    """محاسبه شاخص قدرت نسبی (Relative Strength Index - RSI)"""
    delta = df[price_col].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    rs = gain / loss
    df[f'RSI_{window}'] = 100 - (100 / (1 + rs))
    return df

def calculate_bollinger_bands(df, window=20, num_std=2, price_col='Close'):
    """محاسبه باندهای بولینگر (Bollinger Bands)"""
    sma = df[price_col].rolling(window=window).mean()
    std = df[price_col].rolling(window=window).std()
    
    df[f'BB_Middle_{window}'] = sma
    df[f'BB_Upper_{window}'] = sma + (std * num_std)
    df[f'BB_Lower_{window}'] = sma - (std * num_std)
    return df

def add_all_indicators(df):
    """اضافه کردن تمامی اندیکاتورهای تکنیکال به دیتافریم"""
    if df.empty:
        return df
    
    # کپی برای جلوگیری از هشدار SettingWithCopyWarning
    df = df.copy()
    
    # اگر ستون‌ها MultiIndex هستند، آن‌ها را تخت (flatten) می‌کنیم
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
        
    # اطمینان از نام‌گذاری صحیح ستون Close و تبدیل به عدد
    if 'Close' in df.columns:
        df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    else:
        raise KeyError("ستون Close در داده‌ها یافت نشد.")
    
    # اعمال محاسبات
    df = calculate_sma(df, window=20)
    df = calculate_sma(df, window=50)
    df = calculate_ema(df, window=20)
    df = calculate_rsi(df, window=14)
    df = calculate_bollinger_bands(df, window=20)
    
    # محاسبه بازدهی روزانه (Daily Returns)
    df['Daily_Return'] = df['Close'].pct_change() * 100
    
    return df

if __name__ == "__main__":
    # تست ماژول روی دیتای ذخیره شده بیت‌کوین
    import os
    from fetcher import update_and_save_data
    
    btc_df = update_and_save_data('BTC')
    btc_processed = add_all_indicators(btc_df)
    print("نمونه‌ای از داده‌های پردازش شده با اندیکاتورها:")
    if isinstance(btc_processed.columns, pd.MultiIndex):
        btc_processed.columns = btc_processed.columns.droplevel(0)
    print(btc_processed[['Date', 'Close', 'SMA_20', 'RSI_14', 'Daily_Return']].tail(5))
