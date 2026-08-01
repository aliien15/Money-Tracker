from rich.console import Console
from rich.table import Table
from database import Database

class Ui:
    def print_summary(self, transactions):
        console = Console()
        table = Table(title="Transactions")

        table.add_column("Income", style="green")
        table.add_column("Expenses", style="red")
        table.add_column("Net Savings", style="white")

        database = Database()
        income, expenses, net_savings = database.calculate_summary(transactions)
        
        net_savings_text = text_based_on_amount(net_savings, net_savings >= 0)

        table.add_row(str(income), str(expenses), net_savings_text)

        console.print(table)

    def print_summary_all(self, transactions):
        console = Console()
        table = Table(title="All Transactions")

        table.add_column("ID", style="white")
        table.add_column("Amount", style="white")
        table.add_column("Type", style="white")
        table.add_column("Category", style="white")
        table.add_column("Description", style="white")
        table.add_column("Date", style="white")

        for transaction in transactions:
            amount_text = text_based_on_amount(transaction[1], transaction[2] == "INCOME")

            table.add_row(str(transaction[0]), amount_text, transaction[2], transaction[3], transaction[4], transaction[5])

        console.print(table)

def text_based_on_amount(amount, condition):
    if condition:
        return f"[green]{amount:.2f}[/green]"
    else:
        return f"[red]{amount:.2f}[/red]"