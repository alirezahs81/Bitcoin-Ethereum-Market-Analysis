# 🚀 Cryptocurrency Market Analysis & Dashboard

یک پروژه پایتون پیشرفته، ماژولار و حرفه‌ای برای **تحلیل بازار بیت‌کوین (BTC) و اتریوم (ETH)** همراه با محاسبات تحلیل تکنیکال و یک داشبورد تعاملی وب با استفاده از **Streamlit**.

[![CI](https://github.com/alirezahs81/Bitcoin-Ethereum-Market-Analysis/actions/workflows/ci.yml/badge.svg)](https://github.com/alirezahs81/Bitcoin-Ethereum-Market-Analysis/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-3F4F97?logo=plotly&logoColor=white)

این پروژه به‌گونه‌ای طراحی شده است که علاوه بر داشتن کدهای تمیز و استاندارد، همواره به دیتای زنده بازار متصل بوده و نیازی به فایل‌های CSV ثابت و حجیم ندارد.

---

## 🛠️ قابلیت‌های کلیدی پروژه

1. **دریافت خودکار دیتای زنده (Live Data Fetcher):** اتصال مستقیم به API بازارهای مالی جهت دریافت قیمت‌های تاریخی (OHLCV) بدون نیاز به دانلود دستی.
2. **محاسبات پیشرفته تحلیل تکنیکال (Technical Indicators):**
   * میانگین‌های متحرک ساده و نمایی (`SMA 20/50`, `EMA 20`)
   * شاخص قدرت نسبی (`RSI 14`)
   * باندهای بولینگر (`Bollinger Bands`)
   * محاسبه بازدهی روزانه (`Daily Returns`)
3. **بصری‌سازی حرفه‌ای (Advanced Visualization):** رسم نمودارهای کندل‌استیک دو-بخشی (کندل‌ها + RSI) با تم تاریک (`Dark Theme`) و کاملاً تعاملی به کمک **Plotly**.
4. **داشبورد تعاملی وب (Streamlit Dashboard):** یک وب‌اپلیکیشن کامل برای نمایش کارت‌های آماری (Metrics)، فیلتر بازه‌های زمانی مختلف و مشاهده جدول داده‌ها.

---

## 📁 ساختار پروژه

```text
Bitcoin-Ethereum-Market-Analysis/
│
├── data/                  # ذخیره‌سازی محلی دیتای دریافت شده (خودکار)
├── src/                   # ماژول‌های اصلی پروژه
│   ├── __init__.py
│   ├── fetcher.py         # دریافت و به‌روزرسانی دیتای بازار
│   ├── indicators.py      # توابع محاسباتی تحلیل تکنیکال
│   └── visualizer.py      # رسم نمودارهای تخصصی Plotly
│
├── app.py                 # اپلیکیشن و داشبورد وب با Streamlit
├── requirements.txt       # کتابخانه‌های مورد نیاز پروژه
└── README.md              # مستندات پروژه
```

---

## ⚙️ راهنمای نصب و راه‌اندازی

مراحل زیر را برای اجرای پروژه روی سیستم خود دنبال کنید:

### ۱. کلون کردن ریپازیتوری
```bash
git clone https://github.com/alirezahs81/Bitcoin-Ethereum-Market-Analysis.git
cd Bitcoin-Ethereum-Market-Analysis
```

### ۲. ساخت و فعال‌سازی محیط مجازی (Virtual Environment)
```bash
python -m venv .venv
# در ویندوز:
venv\Scripts\activate
# در لینوکس / مک:
source .venv/bin/activate
```

### ۳. نصب وابستگی‌ها
```bash
pip install -r requirements.txt
```

---

## 🚀 نحوه اجرای پروژه

### اجرای داشبورد وب (Streamlit)
برای باز کردن داشبورد تحلیلی در مرورگر، دستور زیر را اجرا کنید:
```bash
streamlit run app.py
```

پس از اجرای دستور، آدرس لوکال‌هاست (مثل `http://localhost:8501`) در ترمینال نمایش داده می‌شود که با کلیک روی آن می‌توانید وارد داشبورد شوید.


### اجرای تست‌ها (pytest)
```bash
pytest tests/ -v
```

---

## 📊 پیش‌نمایش بخش‌های تحلیل
* **کارت‌های شاخص:** نمایش آنی آخرین قیمت، درصد تغییرات ۲۴ ساعته، بالاترین/پایین‌ترین قیمت روز و وضعیت RSI.
* **نمودار قیمت و اندیکاتورها:** قابلیت زوم، جابجایی و بررسی دقیق روند کندل‌ها در کنار باندهای بولینگر و میانگین‌های متحرک.

---

## 👤 نویسنده و توسعه‌دهنده
توسعه داده شده با ❤️ برای تحلیل‌گران بازار مالی و علاقه‌مندان به علم داده و پایتون.
