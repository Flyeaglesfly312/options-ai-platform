from pathlib import Path
import sys

import streamlit as st


SRC_PATH = Path(__file__).resolve().parent / "src"
sys.path.append(str(SRC_PATH))

from journal import add_journal_entry, list_journal_entries
from risk_rules import can_take_trade


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
    risk_result = can_take_trade(
        potential_loss=potential_loss,
        account_size=account_size,
        risk_percent=risk_percent,
    )

    st.write(f"Maximum Allowed Risk: ${risk_result['max_risk']:.2f}")
    st.write(f"Potential Loss: ${risk_result['potential_loss']:.2f}")

    if risk_result["approved"]:
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
        st.success("Journal entry saved.")
    else:
        st.error("Status: REJECTED")
        st.warning("Journal entry was not saved because it failed the risk check.")

entries = list_journal_entries()

if entries:
    st.table(entries)
else:
    st.info("No journal entries yet.")
