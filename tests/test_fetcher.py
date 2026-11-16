import pytest

from src.fetcher import SYMBOLS, fetch_crypto_data


def test_invalid_symbol_raises():
    with pytest.raises(ValueError):
        fetch_crypto_data("DOGE_FAKE")


def test_symbol_map():
    assert SYMBOLS["BTC"] == "BTC-USD"
    assert SYMBOLS["ETH"] == "ETH-USD"


def test_fetch_btc_live():
    df = fetch_crypto_data("BTC", period="3mo", interval="1d")
    assert not df.empty
    assert {"Date", "Open", "High", "Low", "Close", "Volume"}.issubset(df.columns)
    assert not isinstance(df.columns, __import__("pandas").MultiIndex)
