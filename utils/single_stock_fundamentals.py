# utils/single_stock_fundamentals.py

"""
📈 FundamentalsManager Class - Single Stock Fundamentals Retrieval for Advisory App
---------------------------------------------------------------------------------
Technical Overview:
The FundamentalsManager class retrieves fundamental financial data for a specific stock ticker. 
It uses the YFinance API to fetch current stock data, including price, P/E ratios, market cap, and other relevant metrics. 
The generate_fundamentals_report method compiles these data points into a detailed report that can be used by AgentZero to provide informed responses to the user.

In Simple Terms:
The FundamentalsManager is like a dedicated researcher for a single stock. When a user asks about a specific stock, it gathers up-to-date financial information about that stock, so the app can give the user detailed insights.

Methods:
- generate_fundamentals_report: Fetches stock data using YFinance and compiles it into a report.
"""

import yfinance as yf
import streamlit as st

class FundamentalsManager:
    def generate_fundamentals_report(self, ticker_symbol):
        try:
            stock = yf.Ticker(ticker_symbol)
            info = stock.info
            report = f"""
**{info.get('longName', ticker_symbol.upper())} ({ticker_symbol.upper()})**

- **Current Price:** {info.get('currentPrice', 'N/A')}
- **Market Cap:** {info.get('marketCap', 'N/A')}
- **PE Ratio (TTM):** {info.get('trailingPE', 'N/A')}
- **EPS (TTM):** {info.get('trailingEps', 'N/A')}
- **Dividend Yield:** {info.get('dividendYield', 'N/A')}
- **52 Week High:** {info.get('fiftyTwoWeekHigh', 'N/A')}
- **52 Week Low:** {info.get('fiftyTwoWeekLow', 'N/A')}
- **Sector:** {info.get('sector', 'N/A')}
- **Industry:** {info.get('industry', 'N/A')}
- **Website:** {info.get('website', 'N/A')}

**Business Summary:**
{info.get('longBusinessSummary', 'N/A')}
            """
            return report
        except Exception as e:
            st.error(f"An error occurred while fetching data for {ticker_symbol}: {e}")
            return None
