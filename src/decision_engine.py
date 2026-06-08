def generate_decision(ticker, technical_result, risk_result):
    """Create a simple trade decision from technical analysis and risk checks."""
    # technical_result is expected to come from analyze_ticker() in technical_agent.py.
    # It should include a "technical_score" value from 1 to 10.
    technical_score = technical_result["technical_score"]

    # Higher technical scores create higher confidence in this simple version.
    if technical_score >= 7:
        confidence = 80
    elif technical_score >= 5:
        confidence = 65
    else:
        confidence = 40

    # For now, risk_score uses the same 1-10 value as the technical score.
    risk_score = technical_score

    if risk_result["approved"]:
        # If the risk check passed, the decision engine allows the trade.
        decision = "TRADE"
        reason = "Risk check passed. Technical score included."
    else:
        # If the risk check failed, the decision engine blocks the trade.
        decision = "NO TRADE"
        reason = "Risk check failed. Trade blocked."

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
        "technical_score": 7,
        "trend": "Bullish",
        "reason": "Simulated technical analysis.",
    }

    weak_technical_result = {
        "ticker": "XYZ",
        "technical_score": 4,
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

    print("Strong technical score + approved risk:")
    print(generate_decision("AAPL", strong_technical_result, approved_risk_result))
    print()

    print("Weak technical score + approved risk:")
    print(generate_decision("XYZ", weak_technical_result, approved_risk_result))
    print()

    print("Rejected risk result:")
    print(generate_decision("AAPL", strong_technical_result, rejected_risk_result))
