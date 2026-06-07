from database import get_connection, initialize_database


def add_journal_entry(
    ticker,
    strategy,
    expiration_date,
    strike_price,
    quantity,
    entry_price,
    exit_price=None,
    notes=None,
):
    """Add one trade journal entry to the database."""
    initialize_database()

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO trade_journal (
                ticker,
                strategy,
                expiration_date,
                strike_price,
                quantity,
                entry_price,
                exit_price,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                ticker,
                strategy,
                expiration_date,
                strike_price,
                quantity,
                entry_price,
                exit_price,
                notes,
            ),
        )
        connection.commit()
        return cursor.lastrowid


def list_journal_entries():
    """Return all trade journal entries as easy-to-read dictionaries."""
    initialize_database()

    with get_connection() as connection:
        connection.row_factory = sqlite_row_to_dictionary
        cursor = connection.execute(
            """
            SELECT
                id,
                ticker,
                strategy,
                expiration_date,
                strike_price,
                quantity,
                entry_price,
                exit_price,
                notes,
                created_at
            FROM trade_journal
            ORDER BY created_at DESC, id DESC
            """
        )
        return cursor.fetchall()


def sqlite_row_to_dictionary(cursor, row):
    """Convert one SQLite row into a dictionary using the column names."""
    column_names = [column[0] for column in cursor.description]
    return dict(zip(column_names, row))


def print_journal_entries():
    """Print all trade journal entries in a beginner-friendly format."""
    entries = list_journal_entries()

    if not entries:
        print("No journal entries found.")
        return

    for entry in entries:
        exit_price = entry["exit_price"]
        notes = entry["notes"]

        print(f"Entry #{entry['id']}")
        print(f"Ticker: {entry['ticker']}")
        print(f"Strategy: {entry['strategy']}")
        print(f"Expiration: {entry['expiration_date'] or 'Not provided'}")
        print(f"Strike Price: {entry['strike_price'] or 'Not provided'}")
        print(f"Quantity: {entry['quantity']}")
        print(f"Entry Price: {entry['entry_price']}")
        print(f"Exit Price: {exit_price if exit_price is not None else 'Not closed yet'}")
        print(f"Notes: {notes if notes else 'No notes'}")
        print(f"Created At: {entry['created_at']}")
        print()


if __name__ == "__main__":
    add_journal_entry(
        ticker="AAPL",
        strategy="Covered Call",
        expiration_date="2026-07-17",
        strike_price=200.0,
        quantity=1,
        entry_price=2.5,
        notes="Sample journal entry created from src/journal.py.",
    )

    print_journal_entries()
