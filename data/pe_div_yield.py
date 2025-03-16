import yfinance as yf
import pandas as pd
import os

def get_pe_dividend_marketcap(ticker):
    """
    Fetches the trailing PE, dividend yield, and market cap for the given ticker using Yahoo Finance.
    Returns a dictionary with these values or None if unavailable.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        # Check if essential keys are in info
        # trailingPE and dividendYield might be None if not applicable
        # marketCap should be present if the ticker is valid and data is available
        market_cap = info.get('marketCap', None)
        if market_cap is None:
            return None
        
        pe_ratio = info.get('trailingPE', None)
        dividend_yield = info.get('dividendYield', None)
        
        # Convert dividend_yield to a percentage if needed
        # If dividendYield is e.g. 0.02, meaning 2%, we can either keep it as 0.02 or multiply by 100 to show as %
        # The prompt does not specify which format it prefers, so we'll keep as-is (e.g. 0.02 = 2%)
        
        return {
            'pe_ratio': pe_ratio,
            'dividen_yield': dividend_yield,
            'market_cap_usd': market_cap
        }
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, 'equity_list.csv')
    output_file = os.path.join(script_dir, 'pe_div_yield_table.csv')

    # Read the source CSV
    df = pd.read_csv(input_file)

    # We expect df to have at least these columns: name, ticker, theme, description
    # We'll fetch PE, dividend yield, and market cap from Yahoo Finance
    results = []
    for idx, row in df.iterrows():
        ticker = row['ticker']
        print(f"Processing {ticker}...")
        data = get_pe_dividend_marketcap(ticker)
        if data is None:
            print(f"Skipping {ticker} due to no data returned.")
            continue

        # Prepare the final row
        # Required columns: name, ticker, theme, description, dividen_yield, market_cap_usd, pe_ratio
        final_row = {
            'name': row.get('name', ''),
            'ticker': ticker,
            'theme': row.get('theme', ''),
            'description': row.get('description', ''),
            'dividen_yield': data['dividen_yield'],
            'market_cap_usd': data['market_cap_usd'],
            'pe_ratio': data['pe_ratio']
        }
        results.append(final_row)

    # Create a DataFrame from results
    final_df = pd.DataFrame(results)
    # Exclude stocks that had no data, but we've already done that by skipping them.

    # Sort by market_cap_usd descending
    final_df = final_df.sort_values(by='market_cap_usd', ascending=False)

    # Save to CSV
    final_df.to_csv(output_file, index=False)
    print(f"Saved final dataset to {output_file}")

if __name__ == "__main__":
    main()
