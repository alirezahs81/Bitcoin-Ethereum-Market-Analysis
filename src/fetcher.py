import os
import pandas as pd
import yfinance as yf

# مسیر ذخیره داده‌ها
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

SYMBOLS = {
    'BTC': 'BTC-USD',
    'ETH': 'ETH-USD'
}

def fetch_crypto_data(symbol_key='BTC', period='max', interval='1d'):
    """
    دریافت دیتای تاریخی ارز دیجیتال از Yahoo Finance
    symbol_key: 'BTC' یا 'ETH'
    period: بازه زمانی (مثلاً '1y', '2y', 'max')
    interval: فواصل زمانی (مثلاً '1d', '1h')
    """
    if symbol_key not in SYMBOLS:
        raise ValueError(f"نماد نامعتبر است. نمادهای مجاز: {list(SYMBOLS.keys())}")
    
    ticker = SYMBOLS[symbol_key]
    print(f"در حال دریافت دیتای جدید برای {symbol_key}...")
    
    # استفاده از auto_adjust=False یا روش ایمن‌تر برای جلوگیری از خطای احتمالی yfinance در برخی نسخه‌ها
    df = yf.download(ticker, period=period, interval=interval, progress=False, auto_adjust=True)
    
    if df.empty:
        # تلاش مجدد با پارامترهای پیش‌فرض
        df = yf.download(ticker, period="2y", interval=interval, progress=False)
        
    if df.empty:
        raise Exception(f"خطا در دریافت داده برای {symbol_key}")
    
    # اصلاح ساختار ستون‌های چندسطحی در نسخه جدید yfinance
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
        
    df = df.reset_index(drop=False)
    
    return df

def update_and_save_data(symbol_key='BTC'):
    """
    دریافت دیتای جدید و ذخیره به صورت فایل CSV در پوشه data با قابلیت به‌روزرسانی
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    file_path = os.path.join(DATA_DIR, f"{symbol_key}_data.csv")
    
    # دریافت دیتای جدید با بازه کامل
    df = fetch_crypto_data(symbol_key=symbol_key, period='max', interval='1d')
    
    # ذخیره در فایل CSV
    df.to_csv(file_path, index=False)
    print(f"دیتای {symbol_key} با موفقیت در {file_path} ذخیره شد.")
    return df

if __name__ == "__main__":
    # تست ماژول به صورت مستقل
    for key in SYMBOLS.keys():
        update_and_save_data(key)
