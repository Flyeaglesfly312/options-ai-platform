def analyze_ticker(ticker):
    """Create a simple placeholder technical analysis for a ticker."""
    # This is simulated analysis for now.
    # Later, this function can use real price data and technical indicators.
    first_letter = ticker.upper()[0]

    if "A" <= first_letter <= "M":
        # Tickers starting with A-M get a stronger placeholder score.
        technical_score = 7
        trend = "Bullish"
    else:
        # Tickers starting with N-Z get a neutral placeholder score.
        technical_score = 5
        trend = "Neutral"

    # Return a dictionary so other parts of the app can easily use this analysis.
    return {
        "ticker": ticker,
        "technical_score": technical_score,
        "trend": trend,
        "reason": "Simulated technical analysis.",
    }


if __name__ == "__main__":
    print("NVDA technical analysis:")
    print(analyze_ticker("NVDA"))
    print()

    print("AAPL technical analysis:")
    print(analyze_ticker("AAPL"))
