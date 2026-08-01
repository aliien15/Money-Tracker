import typer
from datetime import date
from database import Database
from ui import Ui

app = typer.Typer()

@app.command()
def log(
        amount: float = typer.Option(..., "--amount", "-a"),
        transaction_type: str = typer.Option(..., "--type", "-t"),
        category: str = typer.Option("General", "--category", "-c"),
        description: str = typer.Option("No description", "--description", "-d"),
        entry_date: str = typer.Option(date.today().isoformat(), "--date", "-D")
        ):
    transaction_type = transaction_type.upper()
    if not is_args_valid(amount, transaction_type, entry_date):
        return
    
    database = Database()
    database.insert_transaction(amount, transaction_type, category, description, entry_date)
    print_success_log_transaction(amount, transaction_type, category, description, entry_date)

def is_args_valid(amount, transaction_type, entry_date):
    if amount <= 0:
        print(f"Invalid amount '{amount}': number must be greater than 0!")
        return False
    
    if transaction_type not in ("INCOME", "EXPENSE"):
        print(f"Invalid transaction type '{transaction_type}'! Valid types: 'INCOME', 'EXPENSE'")
        return False

    try:
        date.fromisoformat(entry_date)
    except ValueError:
        print(f"Invalid date format '{entry_date}'! Please use YYYY-MM-DD (e.g., 2026-08-01).")
        return False

    return True


def print_success_log_transaction(amount, transaction_type, category, description, entry_date):
    print("You have successfully logged a transaction with the following parameters:")
    print(f"Amount: {amount}")
    print(f"Type: {transaction_type}")
    print(f"Category: {category}")
    print(f"Description: {description}")
    print(f"Date: {entry_date}")

@app.command()
def delete(
        id: int = typer.Option(..., "--id", "-i")
        ):
    database = Database()
    rows_deleted = database.delete_transaction(id)

    if rows_deleted == 0:
        print(f"There were no rows with the ID '{id}' to delete!")
    else:
        print(f"The row with ID '{id}' was successfully deleted!")

@app.command()
def summary(
    month: str = typer.Option(date.today().isoformat()[:7], "--month", "-m")
):
    database = Database()
    transactions = database.get_monthly_transactions(month)

    ui = Ui()
    ui.print_summary(transactions)

if __name__ == "__main__":
    app()