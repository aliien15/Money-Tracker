from rich.console import Console
from rich.table import Table
from database import calculate_summary

class Ui:
    def print_summary(self, transactions):
        console = Console()
        table = Table(title="Transactions")

        table.add_column("Income", style="green")
        table.add_column("Expenses", style="red")
        table.add_column("Net Savings", style="white")

        income, expenses, net_savings = calculate_summary(transactions)
        
        net_savings_text = net_savings
        if net_savings >= 0:
            net_savings_text = f"[green]${net_savings:.2f}[/green]"
        else:
            net_savings_text = f"[red]${net_savings:.2f}[/red]"

        table.add_row(str(income), str(expenses), net_savings_text)

        console.print(table)