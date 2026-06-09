from pathlib import Path
import sys

import streamlit as st


SRC_PATH = Path(__file__).resolve().parent / "src"
sys.path.append(str(SRC_PATH))

from journal import add_journal_entry, list_journal_entries
from decision_engine import generate_decision
from risk_rules import can_take_trade
from technical_agent import analyze_ticker


def build_recommendation_report(risk_result, technical_result, decision_result):
    """Create a clear text report that explains the recommendation."""
    if risk_result["approved"]:
        risk_status = "Passed"
    else:
        risk_status = "Failed"

    return f"""Risk Check: {risk_status}

Maximum Allowed Risk: ${risk_result["max_risk"]:.2f}
Potential Loss: ${risk_result["potential_loss"]:.2f}

Technical Score: {technical_result["technical_score"]}
Trend: {technical_result["trend"]}

Analysis:
{technical_result["reason"]}

Final Recommendation:
{decision_result["decision"]}"""


st.title("Options Trade Journal")

with st.form("journal_entry_form"):
    st.subheader("Add Journal Entry")

    ticker = st.text_input("Ticker")
    strategy = st.text_input("Strategy")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    entry_price = st.number_input("Entry Price", min_value=0.0, step=0.01)
    notes = st.text_area("Notes")
    account_size = st.number_input("Account Size", min_value=0.0, value=500.0, step=100.0)
    risk_percent = st.number_input(
        "Risk Percentage",
        min_value=0.0,
        value=0.02,
        step=0.01,
        format="%.2f",
    )
    potential_loss = st.number_input("Potential Loss", min_value=0.0, step=1.0)

    submitted = st.form_submit_button("Save Entry")

if submitted:
    if ticker:
        # Step 1: Analyze the ticker with the Technical Agent.
        technical_result = analyze_ticker(ticker)

        # Step 2: Check whether the trade fits the risk rules.
        risk_result = can_take_trade(
            potential_loss=potential_loss,
            account_size=account_size,
            risk_percent=risk_percent,
        )

        # Step 3: Combine the technical result and risk result into one decision.
        decision_result = generate_decision(
            ticker=ticker,
            technical_result=technical_result,
            risk_result=risk_result,
        )

        st.subheader("Recommendation")
        st.text(build_recommendation_report(risk_result, technical_result, decision_result))
        st.write(f"Confidence: {decision_result['confidence']}")
        st.write(f"Reason: {decision_result['reason']}")

        if decision_result["decision"] == "TRADE":
            st.success("Status: APPROVED")
            add_journal_entry(
                ticker=ticker,
                strategy=strategy,
                expiration_date=None,
                strike_price=None,
                quantity=quantity,
                entry_price=entry_price,
                exit_price=None,
                notes=notes,
            )
            st.success("This trade passed the recommendation checks and was saved to your journal.")
        elif decision_result["decision"] == "WATCHLIST":
            st.info("Status: WATCHLIST")
            st.warning("This setup is interesting, but not strong enough to save as a trade yet.")
        else:
            st.error("Status: REJECTED")
            st.warning("This trade was not saved because the recommendation is NO TRADE.")
    else:
        st.error("Please enter a ticker before saving.")

entries = list_journal_entries()

if entries:
    # Show only the most useful journal columns in the app.
    # The database still keeps all of the original fields.
    display_entries = []

    for entry in entries:
        display_entries.append(
            {
                "ticker": entry["ticker"],
                "strategy": entry["strategy"],
                "quantity": entry["quantity"],
                "entry_price": entry["entry_price"],
                "created_at": entry["created_at"],
            }
        )

    st.dataframe(display_entries, use_container_width=True)
else:
    st.info("No journal entries yet.")
