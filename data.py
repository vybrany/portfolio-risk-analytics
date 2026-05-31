import pandas as pd
import yfinance as yf


def load_prices(tickers):
   

    data = yf.download(
        tickers,
        start="2024-01-01",
        end="2025-01-01",
        auto_adjust=True)

    prices = data["Close"]
    prices = prices.dropna()

    return prices

