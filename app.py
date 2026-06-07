from pathlib import Path
import sys

import streamlit as st


SRC_PATH = Path(__file__).resolve().parent / "src"
sys.path.append(str(SRC_PATH))

from journal import add_journal_entry, list_journal_entries


st.title("Options Trade Journal")

with st.form("journal_entry_form"):
    st.subheader("Add Journal Entry")

    ticker = st.text_input("Ticker")
    strategy = st.text_input("Strategy")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    entry_price = st.number_input("Entry Price", min_value=0.0, step=0.01)
    notes = st.text_area("Notes")

    submitted = st.form_submit_button("Save Entry")

if submitted:
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

entries = list_journal_entries()

if entries:
    st.table(entries)
else:
    st.info("No journal entries yet.")
