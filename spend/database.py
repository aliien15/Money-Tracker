import sqlite3

class Database:

    def __init__(self):
        self.connection = sqlite3.connect("data.db")
        self.db_cursor = self.connection.cursor()

        query = """
            CREATE TABLE IF NOT EXISTS transactions(
            id INTEGER PRIMARY KEY,
            amount REAL NOT NULL,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            date TEXT NOT NULL
            );
        """

        self.db_cursor.execute(query)

    def insert_transaction(self, amount, type, category, description, date):
        self.db_cursor.execute("""
            INSERT INTO transactions(amount, type, category, description, date)
            VALUES (?, ?, ?, ?, ?);
            """,
            (amount, type, category, description, date)
        )

        self.connection.commit()

    def get_monthly_transactions(self, year_month):
        res = self.db_cursor.execute("""
            SELECT * 
            FROM transactions
            WHERE date LIKE ? ||'%';
        """, (year_month,))

        return res.fetchall()

    #  0      1      2       3          4        5
    # (id, amount, type, category, description, date)
    # example = (1, 15.50, "EXPENSE", "Food", "Lunch", "2026-07-02")
    def calculate_summary(transactions):
        income = 0
        expenses = 0

        for transaction in transactions:
            amount = transaction[1]
            transaction_type = transaction[2]

            if transaction_type == "EXPENSE":
                expenses += amount
            else:
                income += amount

        return (income, expenses, income - expenses)
