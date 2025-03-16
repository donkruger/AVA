import yfinance as yf
import pandas as pd
import os

'''
📊 **Piotroski F-Score Calculation Using Open Source APIs** 📈

The **Piotroski F-score** is a financial metric developed by Joseph Piotroski to evaluate the financial health and 
performance of companies. It uses **9 key criteria** grouped into 3 categories: **profitability**, 
**leverage/liquidity/source of funds**, and **operating efficiency**.

---

### 💡 **Calculation Breakdown:**
1️⃣ **Profitability (4 Points)**:
   - ✅ **Positive Net Income**: Net income > 0.
   - 💵 **Positive Operating Cash Flow**: Operating cash flow > 0.
   - 📈 **Increasing ROA (Return on Assets)**: ROA is higher than the previous year.
   - 🔄 **Operating Cash Flow > Net Income**: Indicates strong cash generation.

2️⃣ **Leverage, Liquidity, and Source of Funds (3 Points)**:
   - 💳 **Decrease in Long-Term Debt**: Long-term debt decreased year-over-year.
   - 🚀 **Increase in Current Ratio**: Current assets to liabilities ratio has improved.
   - 🔒 **No New Shares Issued**: Net issuance of shares is ≤ 0.

3️⃣ **Operating Efficiency (2 Points)**:
   - 📊 **Increase in Gross Margin**: Gross profit margin has improved.
   - 🏭 **Increase in Asset Turnover**: Revenue to total assets ratio has increased.

🔢 **Maximum Score**: 9 points, with higher scores indicating better financial health and performance.

---

### 🔧 **How This Script Works with Open Source APIs:**
This script uses **`yfinance`** to gather the required data:

1. **📥 yfinance**:
   - 📑 **Balance Sheet**: Retrieves `Current Assets`, `Current Liabilities`, and `Long-Term Debt`.
   - 🧾 **Income Statement**: Provides `Net Income`, `Gross Profit`, and `Total Revenue`.
   - 💸 **Cash Flow Statement**: Fetches `Operating Cash Flow` and `Issuance/Repurchase of Stock`.

---

### 🛠️ **Step-by-Step Process:**
1️⃣ Fetch financial data for the last two years using **`yfinance`**.
2️⃣ Compute key financial ratios (e.g., ROA, Current Ratio, Gross Margin, Asset Turnover).
3️⃣ Evaluate each of the **9 Piotroski F-score criteria** based on the data.
4️⃣ Aggregate the scores to calculate the final **Piotroski F-score**.
5️⃣ Save the results, including raw data and scores, to a **CSV file** for easy analysis. 📂

---

### 🌟 **Why Use This Script?**
- **Cost-Effective**: Utilizes free and open-source APIs.
- **Scalable**: Analyze multiple companies at once.
- **Insightful**: Quickly assess financial health with a proven methodology.

📁 **Output**:
The enriched CSV includes:
- Raw financial data
- Calculated Piotroski F-score
- Insights to compare the financial health of different companies.

🚀 Use this script to make data-driven decisions and enhance your financial analysis toolkit!
'''
"""
LATEST UPDATE - 11/03/2025
Improved Piotroski F-Score Script
- Ensures proper alignment of dates across Income Statement, Balance Sheet, Cash Flow
- Uses ROA > 0 (instead of just net income > 0)
- Uses (LongTermDebt / TotalAssets) year-over-year comparison

What Changed?
Common Date Intersection
We now gather common_dates = set(financials.columns).intersection(...) across all three DataFrames. This ensures the same exact annual period is used for each statement. We then pick the latest two common dates in descending order.

ROA > 0 for the First Criterion
The original Piotroski approach uses ROA (Return on Assets) > 0 as the profitability measure, not simply Net Income > 0.

Check Decrease in Long-Term Debt Ratio
Instead of just checking if longTermDebt_t < longTermDebt_t1, the script checks (LTD / Total Assets) this year < (LTD / Total Assets) last year.

No Overwriting of “date_t” across statements
Because we use the intersection of columns and pick common_dates_sorted[0] and [1], we safely reference the same exact label (e.g. 2022-12-31) in the Income Statement, Balance Sheet, and Cash Flow.

Net Issuance of Stock
The code still uses issuanceOfStock_t + repurchaseOfStock_t <= 0 as the Piotroski check for “No new shares.” This is standard for an F-score approach using data from the cashflow statement. If you want to use share count changes, you must also fetch the older year’s share count and compare them—but Piotroski’s original measure is simpler and focuses on issuance from the statement of cash flows.

With these tweaks, the script will more faithfully follow Joseph Piotroski’s original 9-point F-score methodology while ensuring correct date alignment from Yahoo Finance’s DataFrames.
"""

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'equity_list.csv')
current_csv = pd.read_csv(file_path)

def get_yfinance_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        print(f"Fetching data for '{ticker}'...")

        # Annual (default) statements
        financials = stock.financials    # Income Statement
        balance_sheet = stock.balance_sheet
        cashflow = stock.cashflow

        # Basic sanity checks
        if financials.empty or balance_sheet.empty or cashflow.empty:
            print(f"No financial data found for ticker '{ticker}'.")
            return {}

        # We want columns (dates) that appear in all three statements
        common_dates = (set(financials.columns)
                        .intersection(set(balance_sheet.columns))
                        .intersection(set(cashflow.columns)))

        # We need at least 2 years (2 columns) to compute a year-over-year Piotroski
        if len(common_dates) < 2:
            print(f"Not enough overlapping annual data for '{ticker}'. Need >= 2 years.")
            return {}

        # Sort the common dates in descending order so index 0 is the most recent year
        common_dates_sorted = sorted(common_dates, reverse=True)

        date_t  = common_dates_sorted[0]  # most recent year
        date_t1 = common_dates_sorted[1]  # prior year

        data = {}

        # ---------- Income Statement Items ----------
        # Net Income
        data['netIncome_t']  = financials.loc['Net Income', date_t]   if 'Net Income' in financials.index else 0.0
        data['netIncome_t1'] = financials.loc['Net Income', date_t1]  if 'Net Income' in financials.index else 0.0

        # Gross Profit
        data['grossProfit_t']  = financials.loc['Gross Profit', date_t]  if 'Gross Profit' in financials.index else 0.0
        data['grossProfit_t1'] = financials.loc['Gross Profit', date_t1] if 'Gross Profit' in financials.index else 0.0

        # Total Revenue
        data['revenue_t']  = financials.loc['Total Revenue', date_t]   if 'Total Revenue' in financials.index else 0.0
        data['revenue_t1'] = financials.loc['Total Revenue', date_t1]  if 'Total Revenue' in financials.index else 0.0

        # ---------- Balance Sheet Items ----------
        data['totalAssets_t']  = balance_sheet.loc['Total Assets', date_t]  if 'Total Assets' in balance_sheet.index else 0.0
        data['totalAssets_t1'] = balance_sheet.loc['Total Assets', date_t1] if 'Total Assets' in balance_sheet.index else 0.0

        data['currentAssets_t']  = balance_sheet.loc['Current Assets', date_t]   if 'Current Assets' in balance_sheet.index else 0.0
        data['currentAssets_t1'] = balance_sheet.loc['Current Assets', date_t1]  if 'Current Assets' in balance_sheet.index else 0.0

        data['currentLiabilities_t']  = balance_sheet.loc['Current Liabilities', date_t]   if 'Current Liabilities' in balance_sheet.index else 0.0
        data['currentLiabilities_t1'] = balance_sheet.loc['Current Liabilities', date_t1]  if 'Current Liabilities' in balance_sheet.index else 0.0

        data['longTermDebt_t']  = balance_sheet.loc['Long Term Debt', date_t]   if 'Long Term Debt' in balance_sheet.index else 0.0
        data['longTermDebt_t1'] = balance_sheet.loc['Long Term Debt', date_t1]  if 'Long Term Debt' in balance_sheet.index else 0.0

        # ---------- Cash Flow Items ----------
        data['operatingCashFlow_t']  = cashflow.loc['Operating Cash Flow', date_t]   if 'Operating Cash Flow' in cashflow.index else 0.0
        data['operatingCashFlow_t1'] = cashflow.loc['Operating Cash Flow', date_t1]  if 'Operating Cash Flow' in cashflow.index else 0.0

        data['issuanceOfStock_t']    = float(cashflow.loc['Issuance Of Capital Stock', date_t]) if 'Issuance Of Capital Stock' in cashflow.index else 0.0
        data['repurchaseOfStock_t']  = float(cashflow.loc['Repurchase Of Capital Stock', date_t]) if 'Repurchase Of Capital Stock' in cashflow.index else 0.0

        data['netIssuanceOfStock_t'] = data['issuanceOfStock_t'] + data['repurchaseOfStock_t']

        # ---------- Ratios ----------
        # ROA
        data['roa_t']  = (data['netIncome_t']  / data['totalAssets_t'])  if data['totalAssets_t']  else 0.0
        data['roa_t1'] = (data['netIncome_t1'] / data['totalAssets_t1']) if data['totalAssets_t1'] else 0.0

        # Current Ratio
        data['currentRatio_t']  = (data['currentAssets_t']  / data['currentLiabilities_t'])  if data['currentLiabilities_t']  else 0.0
        data['currentRatio_t1'] = (data['currentAssets_t1'] / data['currentLiabilities_t1']) if data['currentLiabilities_t1'] else 0.0

        # Gross Margin
        data['grossMargin_t']  = (data['grossProfit_t']  / data['revenue_t'])  if data['revenue_t']  else 0.0
        data['grossMargin_t1'] = (data['grossProfit_t1'] / data['revenue_t1']) if data['revenue_t1'] else 0.0

        # Asset Turnover
        data['assetTurnover_t']  = (data['revenue_t']  / data['totalAssets_t'])  if data['totalAssets_t']  else 0.0
        data['assetTurnover_t1'] = (data['revenue_t1'] / data['totalAssets_t1']) if data['totalAssets_t1'] else 0.0

        return data

    except Exception as e:
        print(f"Error fetching data for '{ticker}': {e}")
        return {}

def calculate_f_score(d):
    """
    Improved Piotroski F-Score Calculation:
      1. ROA > 0
      2. CFO > 0
      3. ΔROA > 0
      4. CFO > Net Income
      5. (LongTermDebt/TotalAssets) T < (LongTermDebt/TotalAssets) T-1
      6. Current Ratio T > Current Ratio T-1
      7. No new shares issued => netIssuanceOfStock_t <= 0
      8. Gross Margin T > Gross Margin T-1
      9. Asset Turnover T > Asset Turnover T-1
    """
    score = 0

    # 1. ROA > 0
    if d.get('roa_t', 0) > 0:
        score += 1

    # 2. CFO > 0
    if d.get('operatingCashFlow_t', 0) > 0:
        score += 1

    # 3. ΔROA > 0 (ROA_t > ROA_t1)
    if d.get('roa_t', 0) > d.get('roa_t1', 0):
        score += 1

    # 4. CFO > Net Income
    if d.get('operatingCashFlow_t', 0) > d.get('netIncome_t', 0):
        score += 1

    # 5. Decrease in Long-Term Debt ratio => (LTD/TA) this year < last year
    ltd_t  = d.get('longTermDebt_t', 0)
    ta_t   = d.get('totalAssets_t', 0)
    ltd_t1 = d.get('longTermDebt_t1', 0)
    ta_t1  = d.get('totalAssets_t1', 0)

    ratio_t  = (ltd_t  / ta_t)  if ta_t  else 0
    ratio_t1 = (ltd_t1 / ta_t1) if ta_t1 else 0

    if ratio_t < ratio_t1:
        score += 1

    # 6. Increase in Current Ratio
    if d.get('currentRatio_t', 0) > d.get('currentRatio_t1', 0):
        score += 1

    # 7. No new shares issued => netIssuanceOfStock_t <= 0
    if d.get('netIssuanceOfStock_t', 0) <= 0:
        score += 1

    # 8. Increase in Gross Margin
    if d.get('grossMargin_t', 0) > d.get('grossMargin_t1', 0):
        score += 1

    # 9. Increase in Asset Turnover
    if d.get('assetTurnover_t', 0) > d.get('assetTurnover_t1', 0):
        score += 1

    return score

enriched_data = []
for index, row in current_csv.iterrows():
    ticker = row['ticker']
    yf_data = get_yfinance_data(ticker)
    if not yf_data:
        print(f"Skipping '{ticker}' due to insufficient data.\n")
        continue

    f_score = calculate_f_score(yf_data)

    # Remove any existing 'f_score' column from the CSV row to avoid confusion
    row = row.drop('f_score', errors='ignore')

    enriched_row = {
        **row,
        **yf_data,
        'f_score': f_score
    }
    enriched_data.append(enriched_row)

    print(f"Calculated Piotroski F-score for '{ticker}': {f_score}\n")

# Create the enriched CSV
output_file = os.path.join(script_dir, 'companies.csv')
enriched_csv = pd.DataFrame(enriched_data)
enriched_csv.to_csv(output_file, index=False)

print(f"\nEnriched fundamentals data saved to '{output_file}'.")
os.system(f"open -a 'Numbers' {output_file}")  # Mac-specific; remove if not needed
