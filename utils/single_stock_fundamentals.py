import yfinance as yf
import streamlit as st

class FundamentalsManager:
    def generate_fundamentals_report(self, ticker_symbol, fundamentals_type=None):
        """
        Generates a fundamentals report for a single stock.

        If 'fundamentals_type' is provided, it may contain one or more metrics,
        e.g. "PE, EBITDA". We parse each metric, lookup in a map,
        and return only those requested metrics if recognized.

        If no recognized items are found, or no fundamentals_type is given,
        we return the full fundamentals report.
        """
        try:
            stock = yf.Ticker(ticker_symbol)
            info = stock.info

            # If the user requested specific fundamentals, handle them:
            if fundamentals_type:
                # 1) Split the string by commas, handle extra whitespace
                requested_fundamentals = [f.strip().lower() for f in fundamentals_type.split(",")]

                # 2) Map user-friendly strings to the actual yfinance info keys
                #    Customize or expand this dictionary as needed.
                fundamentals_map = {
                    "pe": "trailingPE",
                    "p/e": "trailingPE",
                    "currentprice": "currentPrice",
                    "price": "currentPrice",
                    "marketcap": "marketCap",
                    "market cap": "marketCap",
                    "ps": "priceToSalesTrailing12Months",
                    "price to sales": "priceToSalesTrailing12Months",
                    "ebitda": "ebitda",
                    "revenuegrowth": "revenueGrowth",
                    "revenue growth": "revenueGrowth",
                    "grossmargins": "grossMargins",
                    "gross margins": "grossMargins",
                    "fiftytwoweekhigh": "fiftyTwoWeekHigh",
                    "52 week high": "fiftyTwoWeekHigh",
                    "52 week low": "fiftyTwoWeekLow",
                    "fiftytwoweeklow": "fiftyTwoWeekLow",
                    "forwardpe": "forwardPE",
                    "forward pe": "forwardPE",
                    "volume": "volume"
                }

                # 3) Build a list of successfully matched items and any unmatched
                matched_fundamentals = []
                unmatched_fundamentals = []

                for item in requested_fundamentals:
                    # Optionally remove spaces or punctuation
                    # (e.g., "pe" vs. "pe ratio" - you can refine this logic)
                    normalized_item = item.replace(" ", "").replace("ratio", "")
                    
                    yf_key = fundamentals_map.get(normalized_item)
                    if yf_key:
                        value = info.get(yf_key, "N/A")
                        matched_fundamentals.append((item, value))
                    else:
                        unmatched_fundamentals.append(item)

                # 4) If we found any recognized fundamentals, return a short custom report
                if matched_fundamentals:
                    return self._build_custom_report(info, ticker_symbol, matched_fundamentals, unmatched_fundamentals)
                else:
                    # If none matched, fall back to the full fundamentals report
                    return self._generate_full_report(info, ticker_symbol)

            else:
                # If no fundamentals_type is provided, return the full fundamentals.
                return self._generate_full_report(info, ticker_symbol)

        except Exception as e:
            st.error(f"An error occurred while fetching data for {ticker_symbol}: {e}")
            return None

    def _build_custom_report(self, info, ticker_symbol, matched_fundamentals, unmatched_fundamentals):
        """
        Given a list of matched fundamentals (and possibly unmatched),
        build a short custom fundamentals report.
        """
        long_name = info.get('longName', ticker_symbol.upper())
        report = f"**{long_name} ({ticker_symbol.upper()})**\n\n"
        report += "**Requested Fundamentals:**\n"

        for item, val in matched_fundamentals:
            # Display the original item requested (e.g., "PE")
            # Or you can prettify it with item.capitalize(), etc.
            report += f"- **{item}**: {val}\n"

        if unmatched_fundamentals:
            report += "\n**Unrecognized / Unmatched Fundamentals:**\n"
            report += ", ".join(unmatched_fundamentals)

        return report

    def _generate_full_report(self, info, ticker_symbol):
        """
        Helper to generate the full fundamentals report.
        """
        return f"""
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

