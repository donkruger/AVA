import yfinance as yf
import sys

def fetch_historical_prices(ticker, start_date, end_date):
    try:
        # Fetch the historical data
        stock = yf.Ticker(ticker)
        historical_data = stock.history(start=start_date, end=end_date)

        # Check if data exists
        if historical_data.empty:
            print(f"No data found for {ticker} between {start_date} and {end_date}.")
            return

        # Print the historical data
        print(f"Historical prices for {ticker} from {start_date} to {end_date}:\n")
        print(historical_data[['Open', 'High', 'Low', 'Close', 'Volume']])
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Command-line arguments for flexibility
    ticker = input("Enter the stock ticker symbol (e.g., TSLA): ").strip().upper()
    start_date = input("Enter the start date (YYYY-MM-DD): ").strip()
    end_date = input("Enter the end date (YYYY-MM-DD): ").strip()

    fetch_historical_prices(ticker, start_date, end_date)
