# utils/price_chart_manager.py

"""
📈 PriceChartManager Class - Fetching and Displaying Price Charts for Stocks
---------------------------------------------------------------------------
Technical Overview:
The PriceChartManager class retrieves historical price data for a specific stock ticker over a specified period. It uses the yfinance API to fetch the data and returns it in a format suitable for rendering as a chart in Streamlit.

In Simple Terms:
PriceChartManager is like a tool that gets the stock price history so we can show it as a chart to the user when they ask for it.

Methods:
- get_price_data: Fetches historical price data using yfinance.
- prepare_chart: Returns the data ready for Streamlit to render.
"""
import yfinance as yf
import pandas as pd

class PriceChartManager:
    def get_price_data(self, ticker_symbol, period='1mo'):
        try:
            # Fetch the historical data
            stock = yf.Ticker(ticker_symbol)
            historical_data = stock.history(period=period)

            # Check if data exists
            if historical_data.empty:
                return None, None, f"No data found for {ticker_symbol} over the period {period}."

            # Extract the latest price
            latest_price = historical_data['Close'].iloc[-1]

            # Return the historical data and latest price
            return historical_data, latest_price, None
        except Exception as e:
            return None, None, f"An error occurred while fetching data for {ticker_symbol}: {e}"

