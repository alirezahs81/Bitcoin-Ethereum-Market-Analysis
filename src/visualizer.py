import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_crypto_analysis(df, symbol_name="BTC"):
    """
    رسم نمودار پیشرفته کندل‌استیک به همراه میانگین‌های متحرک، باندهای بولینگر و RSI
    """
    if df.empty:
        raise ValueError("داده‌ای برای رسم نمودار وجود ندارد.")
    
    # اطمینان از مسطح بودن ستون‌ها
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
        
    # ساخت یک مینی-رابط با دو ساب‌پات (بالایی: قیمت و اندیکاتورها، پایینی: RSI)
    fig = make_subplots(
        rows=2, cols=1, 
        vertical_spacing=0.05,
        row_heights=[0.7, 0.3],
        subplot_titles=(f'{symbol_name} Price & Technical Indicators', 'Relative Strength Index (RSI)')
    )
    
    # ۱. نمودار کندل‌استیک قیمت
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
    
    # ۲. میانگین متحرک SMA 20
    if 'SMA_20' in df.columns:
        fig.add_trace(
            go.Scatter(x=df['Date'], y=df['SMA_20'], line=dict(color='orange', width=1.5), name='SMA 20'),
            row=1, col=1
        )
        
    # ۳. باندهای بولینگر
    if 'BB_Upper_20' in df.columns and 'BB_Lower_20' in df.columns:
        fig.add_trace(
            go.Scatter(x=df['Date'], y=df['BB_Upper_20'], line=dict(color='gray', width=1, dash='dash'), name='BB Upper'),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=df['Date'], y=df['BB_Lower_20'], line=dict(color='gray', width=1, dash='dash'), name='BB Lower', fill='tonexty', fillcolor='rgba(200,200,200,0.1)'),
            row=1, col=1
        )

    # ۴. اندیکاتور RSI در ساب‌پات پایینی
    if 'RSI_14' in df.columns:
        fig.add_trace(
            go.Scatter(x=df['Date'], y=df['RSI_14'], line=dict(color='purple', width=1.5), name='RSI (14)'),
            row=2, col=1
        )
        # خطوط راهنمای اشباع خرید (70) و اشباع فروش (30)
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

    # تنظیمات کلی ظاهر نمودار (Dark Theme جذاب برای کریپتو)
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
    from fetcher import update_and_save_data
    from indicators import add_all_indicators
    
    # تست ماژول
    df = update_and_save_data('BTC')
    df = add_all_indicators(df)
    
    fig = plot_crypto_analysis(df, "BTC")
    # ذخیره به صورت فایل HTML برای بررسی
    fig.write_html("btc_analysis.html")
    print("نمودار با موفقیت رسم و در فایل btc_analysis.html ذخیره شد.")
