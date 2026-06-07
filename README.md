# Options AI Platform

Options AI Platform is a decision-support system for options traders. The platform is designed to evaluate trade ideas, apply risk controls, maintain an auditable journal, and eventually incorporate AI-assisted analysis and recommendation workflows.

Right now, the project lets you save simple trade journal entries in a local
SQLite database and view them in a small Streamlit web app.

This is an early version of the project. The goal is to slowly build it into a
tool that helps track trades, review decisions, and eventually analyze risk.

## What This Project Does

This project stores options trade journal entries.

Each entry can include:

- Ticker symbol
- Strategy
- Quantity
- Entry price
- Notes
- Created timestamp

The data is saved locally in:

```text
database/options_platform.db
```

That file is a SQLite database. SQLite is a small database system that stores
data in a normal file on your computer.

## How To Install

First, open a terminal in this project folder.

Then create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install Streamlit:

```bash
pip install streamlit
```

If more packages are added later, they should be listed in `requirements.txt`.

## How To Run

Start the Streamlit app:

```bash
streamlit run app.py
```

Then open the local URL shown in your terminal. It will usually be:

```text
http://localhost:8501
```

## Current Features

- Create a local SQLite database
- Create a `trade_journal` table
- Add a journal entry from Python
- List all journal entries from Python
- Print journal entries in a beginner-friendly format
- View journal entries in a Streamlit table
- Add a new journal entry from the Streamlit app

## Project Structure

```text
app.py
src/
  database.py
  journal.py
  risk_rules.py
database/
data/
tests/
```

Important files:

- `app.py` runs the Streamlit web app.
- `src/database.py` creates and connects to the SQLite database.
- `src/journal.py` adds, lists, and prints journal entries.
- `src/risk_rules.py` is reserved for future risk checks.
- `database/options_platform.db` stores local journal data.

## Future Roadmap

Planned next steps:

- Add expiration date and strike price fields to the Streamlit form
- Add an exit price field for closed trades
- Add validation so blank tickers and strategies cannot be saved
- Add basic profit and loss tracking
- Add risk rules for position size and max loss
- Add charts for journal history
- Add tests for the database and journal functions
- Add all required packages to `requirements.txt`

## Beginner Notes

This project is intentionally small.

The main idea is:

1. `app.py` shows the web page.
2. `src/journal.py` handles journal actions.
3. `src/database.py` handles database setup and connections.
4. SQLite stores the data locally.

Keeping these jobs separate makes the code easier to understand and easier to
improve later.
