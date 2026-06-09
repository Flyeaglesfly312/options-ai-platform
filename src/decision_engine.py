def generate_decision(ticker, technical_result, risk_result):
    """Create a simple trade decision from technical analysis and risk checks."""
    # technical_result is expected to come from analyze_ticker() in technical_agent.py.
    # It should include a "technical_score" value from 1 to 10.
    technical_score = technical_result["technical_score"]

    # Confidence is based on the technical score.
    # Example: technical_score 8 becomes confidence 80.
    confidence = technical_score * 10

    # For now, risk_score uses the same 1-10 value as the technical score.
    risk_score = technical_score

    if risk_result["approved"] is False:
        # If the risk check fails, the trade is blocked no matter what.
        decision = "NO TRADE"
        reason = "Risk check failed. Trade blocked."
    elif technical_score >= 7:
        # Strong technical scores can become trade ideas when risk is approved.
        decision = "TRADE"
        reason = "Risk check passed and technical score is strong."
    elif technical_score >= 5:
        # Medium technical scores are worth watching, but not trading yet.
        decision = "WATCHLIST"
        reason = "Risk check passed, but technical score is only moderate."
    else:
        # Weak technical scores are rejected even when risk is approved.
        decision = "NO TRADE"
        reason = "Risk check passed, but technical score is weak."

    # Return a dictionary so other parts of the app can easily use this result.
    return {
        "ticker": ticker,
        "decision": decision,
        "confidence": confidence,
        "risk_score": risk_score,
        "reason": reason,
    }


if __name__ == "__main__":
    strong_technical_result = {
        "ticker": "AAPL",
        "technical_score": 8,
        "trend": "Bullish",
        "reason": "Simulated technical analysis.",
    }

    moderate_technical_result = {
        "ticker": "MSFT",
        "technical_score": 5,
        "trend": "Neutral",
        "reason": "Simulated technical analysis.",
    }

    weak_technical_result = {
        "ticker": "XYZ",
        "technical_score": 3,
        "trend": "Bearish",
        "reason": "Simulated technical analysis.",
    }

    approved_risk_result = {
        "approved": True,
        "max_risk": 10,
        "potential_loss": 8,
        "message": "Trade approved. Potential loss is within your risk limit.",
    }

    rejected_risk_result = {
        "approved": False,
        "max_risk": 10,
        "potential_loss": 15,
        "message": "Trade rejected. Potential loss is higher than your risk limit.",
    }

    print("TRADE example:")
    print(generate_decision("AAPL", strong_technical_result, approved_risk_result))
    print()

    print("WATCHLIST example:")
    print(generate_decision("MSFT", moderate_technical_result, approved_risk_result))
    print()

    print("NO TRADE example:")
    print(generate_decision("XYZ", weak_technical_result, approved_risk_result))
    print()

    print("NO TRADE example because risk failed:")
    print(generate_decision("AAPL", strong_technical_result, rejected_risk_result))
