# 🚀 Cryptocurrency Market Analysis & Dashboard

[![CI](https://github.com/alirezahs81/Bitcoin-Ethereum-Market-Analysis/actions/workflows/ci.yml/badge.svg)](https://github.com/alirezahs81/Bitcoin-Ethereum-Market-Analysis/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-3F4F97?logo=plotly&logoColor=white)

An advanced, modular and professional Python project for **analyzing the Bitcoin (BTC) and Ethereum (ETH) markets** with technical indicator calculations and an interactive web dashboard built with **Streamlit**.

The project is designed to always stay connected to live market data with clean, standard code — no need for fixed, heavyweight CSV files.

---

## 🛠️ Key Features

1. **Live Data Fetcher:** direct connection to market APIs for historical OHLCV prices, no manual downloads needed.
2. **Advanced Technical Indicators:**
   * Simple and exponential moving averages (`SMA 20/50`, `EMA 20`)
   * Relative Strength Index (`RSI 14`)
   * Bollinger Bands
   * Daily returns calculation
3. **Advanced Visualization:** two-panel interactive candlestick charts (candles + RSI) with a dark theme, powered by **Plotly**.
4. **Streamlit Dashboard:** a complete web app with metric cards, multiple time-frame filters and a data table view.

---

## 📁 Project Structure

```text
Bitcoin-Ethereum-Market-Analysis/
│
├── data/                  # Local storage for fetched market data (automatic)
├── src/                   # Core project modules
│   ├── __init__.py
│   ├── fetcher.py         # Market data fetching & updating
│   ├── indicators.py      # Technical analysis calculations
│   └── visualizer.py      # Professional Plotly charts
│
├── tests/                 # Automated pytest suite
├── .github/workflows/     # CI with GitHub Actions
├── app.py                 # Streamlit web dashboard
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

---

## ⚙️ Installation & Setup

Follow these steps to run the project on your machine:

### 1. Clone the repository
```bash
git clone https://github.com/alirezahs81/Bitcoin-Ethereum-Market-Analysis.git
cd Bitcoin-Ethereum-Market-Analysis
```

### 2. Create and activate a virtual environment
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/Mac:
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Project

### Launch the web dashboard (Streamlit)
To open the analytical dashboard in your browser, run:
```bash
streamlit run app.py
```

A local address (like `http://localhost:8501`) appears in the terminal — click it to open the dashboard.

### Run the tests (pytest)
```bash
pytest tests/ -v
```

---

## 📊 What the Dashboard Shows
* **Metric cards:** instant view of the latest price, 24h change %, daily high/low and RSI status.
* **Price & indicators chart:** zoom, pan and detailed trend inspection of candles alongside Bollinger Bands and moving averages.

---

## 🧪 Testing

The repository ships with an 11-test pytest suite covering the indicator math (on synthetic data) and the live fetcher, executed automatically by GitHub Actions on every push.

---

## 👤 Author

Built with ❤️ for financial market analysts and data science enthusiasts.
