def generate_decision(ticker, risk_result):
    """Create a simple trade decision from a risk check result."""
    # risk_result is expected to come from can_take_trade() in risk_rules.py.
    # It should include an "approved" value that is either True or False.
    approved = risk_result["approved"]

    if approved:
        # If the risk check passed, the decision engine allows the trade.
        decision = "TRADE"
        confidence = 75
        risk_score = 8
        reason = "Risk check passed."
    else:
        # If the risk check failed, the decision engine blocks the trade.
        decision = "NO TRADE"
        confidence = 30
        risk_score = 3
        reason = "Risk check failed."

    # Return a dictionary so other parts of the app can easily use this result.
    return {
        "ticker": ticker,
        "decision": decision,
        "confidence": confidence,
        "risk_score": risk_score,
        "reason": reason,
    }


if __name__ == "__main__":
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

    print("Approved trade decision:")
    print(generate_decision("NVDA", approved_risk_result))
    print()

    print("Rejected trade decision:")
    print(generate_decision("TSLA", rejected_risk_result))
