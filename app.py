import streamlit as st
import pandas as pd
import os

from src.fetcher import update_and_save_data, SYMBOLS
from src.indicators import add_all_indicators
from src.visualizer import plot_crypto_analysis

# تنظیمات صفحه Streamlit
st.set_page_config(
    page_title="Crypto Market Analysis Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("🚀 Cryptocurrency Market Analysis Dashboard")
st.markdown("تحلیل جامع بازار بیت‌کوین و اتریوم همراه با اندیکاتورهای تکنیکال پیشرفته")

# نوار کناری (Sidebar) برای تنظیمات
st.sidebar.header("تنظیمات داشبورد")

selected_symbol = st.sidebar.selectbox(
    "انتخاب ارز دیجیتال:",
    options=list(SYMBOLS.keys()),
    format_func=lambda x: "Bitcoin (BTC)" if x == "BTC" else "Ethereum (ETH)"
)

if st.sidebar.button("🔄 به‌روزرسانی دیتای زنده"):
    with st.spinner("در حال دریافت آخرین داده‌ها از بازار..."):
        try:
            update_and_save_data(selected_symbol)
            st.sidebar.success("داده‌ها با موفقیت به‌روزرسانی شدند!")
        except Exception as e:
            st.sidebar.error(f"خطا در به‌روزرسانی: {e}")

# بارگذاری داده‌ها
data_path = os.path.join(os.path.dirname(__file__), 'data', f"{selected_symbol}_data.csv")

if not os.path.exists(data_path):
    with st.spinner(f"داده‌ای یافت نشد. در حال دریافت اولیه دیتای {selected_symbol}..."):
        try:
            update_and_save_data(selected_symbol)
        except Exception as e:
            st.error(f"خطا در دانلود داده: {e}")

if os.path.exists(data_path):
    df = pd.read_csv(data_path)
    
    # اعمال اندیکاتورها
    df = add_all_indicators(df)
    
    # نمایش معیارهای کلیدی (Metrics) در بالای صفحه
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    
    price_change = latest['Close'] - prev['Close']
    price_change_pct = (price_change / prev['Close']) * 100
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("آخرین قیمت (USD)", f"${latest['Close']:,.2f}", f"{price_change_pct:.2f}%")
    col2.metric("بالاترین قیمت روز", f"${latest['High']:,.2f}")
    col3.metric("پایین‌ترین قیمت روز", f"${latest['Low']:,.2f}")
    col4.metric("شاخص RSI (14)", f"{latest.get('RSI_14', 0):.2f}")
    
    st.markdown("---")
    
    # انتخاب بازه زمانی نمایشی روی نمودار
    timeframe = st.sidebar.radio(
        "بازه زمانی نمایش نمودار:",
        options=['1 ماهه', '3 ماهه', '6 ماهه', '1 ساله', 'همه تاریخچه'],
        index=3
    )
    
    filtered_df = df.copy()
    filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
    
    if timeframe == '1 ماهه':
        filtered_df = filtered_df.tail(30)
    elif timeframe == '3 ماهه':
        filtered_df = filtered_df.tail(90)
    elif timeframe == '6 ماهه':
        filtered_df = filtered_df.tail(180)
    elif timeframe == '1 ساله':
        filtered_df = filtered_df.tail(365)
        
    # رسم نمودار Plotly
    fig = plot_crypto_analysis(filtered_df, selected_symbol)
    st.plotly_chart(fig, use_container_width=True)
    
    # نمایش جدول داده‌های اخیر
    with st.expander("📁 مشاهده جدول داده‌های خام و اندیکاتورها"):
        st.dataframe(df.tail(50).sort_index(ascending=False))

else:
    st.warning("لطفاً ابتدا دیتای ارز مورد نظر را دریافت کنید.")
