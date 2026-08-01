# 💸 Spending CLI

A modern, terminal-based personal finance and transaction tracking CLI built with **Python**.

This CLI lets you log income and expenses, inspect transaction information, and view financial summaries directly from your terminal! All the data is saved in a local SQLite database, which requires 0 extra setup!

---

## ✨ Features

* **Strict Input Validation:** Automatically validates positive amounts, normalizes transaction types (`INCOME`/`EXPENSE`), and verifies ISO date formats (`YYYY-MM-DD`) before touching the database.
* **Beautiful Terminal UI:** Used the `Rich` library to render clean, color-coded transaction tables and financial summaries (green for income, red for expenses, dynamic color-coding for net savings).
* **Zero-Config Database:** Uses SQLite (`data.db`) with automatic table creation (`IF NOT EXISTS`) and safe, parameterized queries (`?`) to prevent SQL injection.
* **Modular MVC Design:** Clear separation of concerns between database queries (`Model`), Rich presentation rendering (`View`), and CLI command routing (`Controller`).

---

## 🏗️ Architecture & Project Structure

```text
spend-cli/
├── spend/
│   ├── cli.py        # Controller: Typer command registration & input validation
│   ├── database.py   # Model: SQLite schema, CRUD operations & aggregation logic
│   ├── ui.py         # View: Rich table formatting & dynamic color rendering
├── tests/            # Automated test suites for CLI, database, and UI logic
├── README.md
└── .gitignore

---

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/aliien15/Spend-CLI.git](https://github.com/aliien15/Spend-CLI.git)
   cd spend-cli
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install typer rich
   ```

---

## 📖 Command Reference

All commands are run via the main entry point in `spend/cli.py`.

| Command | Description | Key Options / Flags | Default Value |
| :--- | :--- | :--- | :--- |
| **`log`** | Log a new income or expense transaction | `-a` / `--amount`<br>`-t` / `--type`<br>`-c` / `--category`<br>`-d` / `--description`<br>`-D` / `--date` | *Required*<br>*Required*<br>`"General"`<br>`"No description"`<br>`Today (YYYY-MM-DD)` |
| **`delete`** | Delete a specific transaction by its ID | `-i` / `--id` | *Required* |
| **`deleteall`** | Permanently remove all logged transactions | *None* | — |
| **`summary`** | View monthly totals (Income, Expenses, Net) | `-m` / `--month` | `Current Month (YYYY-MM)` |
| **`summaryall`** | View all-time financial summary totals | *None* | — |
| **`transactionsall`** | Print a detailed ledger table of every transaction | *None* | — |

---

## 💡 Usage Examples

### Log an Expense (with custom date and description)
```bash
python spend/cli.py log -a 15.50 -t expense -c "Food" -d "Lunch with friends" -D 2026-08-01
```

### Log Income (using defaults for category, description, and today's date)
```bash
python spend/cli.py log -a 1200.00 -t income
```

### View Monthly Summary for August 2026
```bash
python spend/cli.py summary -m 2026-08
```

### Display the Full All-Time Transaction Ledger
```bash
python spend/cli.py transactionsall
```

### Delete a Specific Transaction by ID
```bash
python spend/cli.py delete -i 3
```

---

## 🛠️ Built With

* **[Python 3](https://www.python.org/)** - Standard Library (`sqlite3`, `datetime`)
* **[Typer](https://typer.tiangolo.com/)** - Modern CLI application builder
* **[Rich](https://rich.readthedocs.io/)** - Rich text and table rendering in the terminal