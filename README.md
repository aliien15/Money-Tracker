# 💸 Money Tracker

A modern personal finance and transaction tracking application built with **Python**, featuring both a **simple Desktop GUI** and a **powerful Terminal CLI**.

Whether you prefer clicking through a clean dark-mode desktop interface or running rapid terminal commands, this app lets you log income and expenses, inspect transaction history, and view real-time financial summaries—all backed by a zero-configuration local SQLite database!

---

## ✨ Features

### 🖥️ Desktop GUI
* **Modern Dark/Light Mode UI:** Built for a simple, system-aware aesthetic that looks great on Windows, macOS, and Linux.
* **Real-Time Financial Dashboard:** Instantly view color-coded summary cards for **Total Income**, **Total Expenses**, and **Net Balance** that automatically refresh whenever data changes.
* **Interactive Multi-Column Grid:** Browse transactions in a responsive spreadsheet-style layout with expanding description columns and inline **Delete** buttons for quick management.
* **Input Validation & Safety:** Catch formatting errors early with built-in checks for numerical amounts (`XXXX.XX`) and ISO dates (`YYYY-MM-DD`).

### ⌨️ Terminal CLI
* **Rapid Terminal Logging:** Log transactions, inspect ledgers, and check monthly summaries without leaving your command line.
* **Beautiful Terminal Formatting:** Uses the `Rich` library to render tables and visual indicators.
* **Strict Command Validation:** Built-in validation ensures clean data entry before touching the database.

### 🗄️ Zero-Config Database
* **Local SQLite Storage:** Uses a single `data.db` file with zero setup required.
* **SQL-Level Sorting & Optimization:** Automatically sorts your transactions from newest to oldest to ensure accurate chronological ordering.
* **SQL Injection Prevention:** 100% parameterized queries (`?`) for safe and reliable data handling.

---

## 🏗️ Architecture & Project Structure

```text
spend-cli/
├── spend/
│   ├── interface.py  # Desktop GUI: CustomTkinter multi-tab interface & dashboard
│   ├── cli.py        # CLI Controller: Typer command registration & validation
│   ├── database.py   # Model: SQLite schema, CRUD operations & aggregation logic
│   ├── ui.py         # CLI View: Rich table formatting & terminal color rendering
├── tests/            # Automated test suites for database, GUI, and CLI logic
├── README.md
└── .gitignore
```

---

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/aliien15/Money-Tracker.git](https://github.com/aliien15/Money-Tracker.git)
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
   pip install typer rich customtkinter
   ```

---

## 🖥️ Launching the Desktop Application

To open the graphical desktop interface, run:

```bash
python spend/interface.py
```

* **Add Tab:** Enter an amount, select `INCOME` or `EXPENSE`, add an optional category/description, and save.
* **History Tab:** Scroll through your sorted ledger and remove entries using the inline **Delete** buttons.
* **Summary Tab:** Check your real-time **Total Income**, **Total Expenses**, and **Net Balance** dashboard cards.

---

## 📖 CLI Command Reference

All command-line operations are executed via `spend/cli.py`.

| Command | Description | Key Options / Flags | Default Value |
| :--- | :--- | :--- | :--- |
| **`log`** | Log a new income or expense transaction | `-a` / `--amount`<br>`-t` / `--type`<br>`-c` / `--category`<br>`-d` / `--description`<br>`-D` / `--date` | *Required*<br>*Required*<br>`"General"`<br>`"No description"`<br>`Today (YYYY-MM-DD)` |
| **`delete`** | Delete a specific transaction by its ID | `-i` / `--id` | *Required* |
| **`deleteall`** | Permanently remove all logged transactions | *None* | — |
| **`summary`** | View monthly totals (Income, Expenses, Net) | `-m` / `--month` | `Current Month (YYYY-MM)` |
| **`summaryall`** | View all-time financial summary totals | *None* | — |
| **`transactionsall`** | Print a detailed ledger table of every transaction | *None* | — |

---

## 💡 CLI Usage Examples

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
* **[CustomTkinter](https://customtkinter.tomschimansky.com/)** - Modern, dark-mode desktop GUI framework
* **[Typer](https://typer.tiangolo.com/)** - Modern CLI application builder
* **[Rich](https://rich.readthedocs.io/)** - Rich text and table rendering in the terminal