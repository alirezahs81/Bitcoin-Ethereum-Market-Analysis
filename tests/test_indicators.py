import numpy as np
import pandas as pd
import pytest

from src.indicators import (
    add_all_indicators,
    calculate_bollinger_bands,
    calculate_ema,
    calculate_rsi,
    calculate_sma,
)


@pytest.fixture
def ohlcv_df() -> pd.DataFrame:
    """Synthetic 120-day OHLCV frame with a deterministic random walk."""
    rng = np.random.default_rng(42)
    steps = rng.normal(loc=0.0, scale=1.0, size=120)
    close = 50000 + np.cumsum(steps * 100)
    high = close + np.abs(rng.normal(50, 20, size=120))
    low = close - np.abs(rng.normal(50, 20, size=120))
    open_ = (high + low) / 2
    return pd.DataFrame(
        {
            "Date": pd.date_range("2025-01-01", periods=120, freq="D"),
            "Open": open_,
            "High": high,
            "Low": low,
            "Close": close,
            "Volume": rng.integers(1000, 5000, size=120).astype(float),
        }
    )


def test_calculate_sma(ohlcv_df):
    result = calculate_sma(ohlcv_df, window=20)
    expected = ohlcv_df["Close"].rolling(20).mean()
    assert "SMA_20" in result.columns
    pd.testing.assert_series_equal(result["SMA_20"], expected, check_names=False)


def test_calculate_ema(ohlcv_df):
    result = calculate_ema(ohlcv_df, window=20)
    expected = ohlcv_df["Close"].ewm(span=20, adjust=False).mean()
    assert "EMA_20" in result.columns
    pd.testing.assert_series_equal(result["EMA_20"], expected, check_names=False)


def test_calculate_rsi_bounds(ohlcv_df):
    result = calculate_rsi(ohlcv_df, window=14)
    rsi = result["RSI_14"].dropna()
    assert "RSI_14" in result.columns
    assert ((rsi >= 0) & (rsi <= 100)).all()


def test_bollinger_bands_ordering(ohlcv_df):
    result = calculate_bollinger_bands(ohlcv_df, window=20, num_std=2)
    valid = result.dropna(subset=["BB_Upper_20", "BB_Lower_20"])
    assert (valid["BB_Upper_20"] >= valid["BB_Middle_20"]).all()
    assert (valid["BB_Middle_20"] >= valid["BB_Lower_20"]).all()


def test_add_all_indicators(ohlcv_df):
    result = add_all_indicators(ohlcv_df)
    expected_cols = [
        "SMA_20", "SMA_50", "EMA_20", "RSI_14",
        "BB_Middle_20", "BB_Upper_20", "BB_Lower_20", "Daily_Return",
    ]
    for col in expected_cols:
        assert col in result.columns, f"missing indicator column: {col}"
    # Early rows before the windows fill up must be NaN, not garbage
    assert result["SMA_50"].iloc[:49].isna().all()


def test_add_all_indicators_empty_df():
    assert add_all_indicators(pd.DataFrame()).empty


def test_add_all_indicators_missing_close_raises():
    with pytest.raises(KeyError):
        add_all_indicators(pd.DataFrame({"Date": [1, 2, 3]}))


def test_add_all_indicators_flattens_multiindex(ohlcv_df):
    multi = ohlcv_df.copy()
    multi.columns = pd.MultiIndex.from_tuples(
        [(c, "BTC-USD") for c in multi.columns]
    )
    result = add_all_indicators(multi)
    assert "RSI_14" in result.columns
