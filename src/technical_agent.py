import yfinance as yf


def analyze_ticker(ticker):
    """Analyze a ticker using simple moving averages from real price data."""
    # Keep ticker symbols consistent, even if the user types lowercase letters.
    ticker = ticker.upper()

    # yfinance downloads historical stock price data from Yahoo Finance.
    # Six months gives us enough daily candles to calculate a 50-day average.
    price_data = yf.download(ticker, period="6mo", interval="1d", progress=False)

    if hasattr(price_data.columns, "nlevels") and price_data.columns.nlevels > 1:
        # Some yfinance versions return grouped columns for a ticker.
        # This keeps the table easy to use, with simple names like "Close".
        price_data.columns = price_data.columns.get_level_values(0)

    if price_data.empty:
        # If no data comes back, return a clear result instead of crashing.
        return {
            "ticker": ticker,
            "technical_score": 1,
            "trend": "Unknown",
            "reason": "No price data was found for this ticker.",
        }

    if len(price_data) < 50:
        # A 50-day moving average needs at least 50 daily prices.
        return {
            "ticker": ticker,
            "technical_score": 2,
            "trend": "Unknown",
            "reason": "Not enough price data to calculate the 50-day moving average.",
        }

    # Moving averages smooth out daily price movement.
    # The 20-day average is shorter-term, and the 50-day average is longer-term.
    price_data["MA20"] = price_data["Close"].rolling(window=20).mean()
    price_data["MA50"] = price_data["Close"].rolling(window=50).mean()

    latest_row = price_data.iloc[-1]
    current_price = latest_row["Close"]
    moving_average_20 = latest_row["MA20"]
    moving_average_50 = latest_row["MA50"]

    if current_price > moving_average_20 and current_price > moving_average_50:
        # Price above both moving averages is treated as bullish.
        technical_score = 8
        trend = "Bullish"
        reason = "Current price is above the 20-day and 50-day moving averages."
    elif min(moving_average_20, moving_average_50) <= current_price <= max(
        moving_average_20,
        moving_average_50,
    ):
        # Price between the moving averages is treated as neutral.
        technical_score = 5
        trend = "Neutral"
        reason = "Current price is between the 20-day and 50-day moving averages."
    else:
        # Price below both moving averages is treated as bearish.
        technical_score = 3
        trend = "Bearish"
        reason = "Current price is below the 20-day and 50-day moving averages."

    # Return a dictionary so other parts of the app can easily use this analysis.
    return {
        "ticker": ticker,
        "technical_score": technical_score,
        "trend": trend,
        "reason": reason,
    }


if __name__ == "__main__":
    print("NVDA technical analysis:")
    print(analyze_ticker("NVDA"))
    print()

    print("AAPL technical analysis:")
    print(analyze_ticker("AAPL"))
