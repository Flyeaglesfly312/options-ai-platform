def calculate_max_risk(account_size, risk_percent):
    """Calculate the most money you are willing to risk on one trade."""
    # Example: a $500 account with 2% risk means 500 * 0.02 = $10 max risk.
    return account_size * risk_percent


def can_take_trade(potential_loss, account_size, risk_percent):
    """Decide whether a trade fits inside your risk limit."""
    # First, calculate the maximum amount this account should risk.
    max_risk = calculate_max_risk(account_size, risk_percent)

    # A trade is approved only when the possible loss is not above max risk.
    approved = potential_loss <= max_risk

    if approved:
        message = "Trade approved. Potential loss is within your risk limit."
    else:
        message = "Trade rejected. Potential loss is higher than your risk limit."

    # Return a dictionary so the result is easy to read and easy to use later.
    return {
        "approved": approved,
        "max_risk": max_risk,
        "potential_loss": potential_loss,
        "message": message,
    }


if __name__ == "__main__":
    account_size = 500
    risk_percent = 0.02

    print("Maximum risk example:")
    print(calculate_max_risk(account_size, risk_percent))
    print()

    print("Approved trade example:")
    print(can_take_trade(8, account_size, risk_percent))
    print()

    print("Rejected trade example:")
    print(can_take_trade(15, account_size, risk_percent))
