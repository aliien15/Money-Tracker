from spend.database import Database
from datetime import date
from hypothesis import given, strategies as st

@given(
    transactions=st.lists(
        st.tuples(
            st.floats(min_value=0.01, max_value=500.0),
            st.sampled_from(["INCOME", "EXPENSE"]),
            st.text(min_size=1, max_size=20)
        ),
        min_size=1,
        max_size=20
    )
)
def test_calculate_summary(transactions):
    database = Database(":memory:")

    for transaction in transactions:
        database.insert_transaction(transaction[0], transaction[1], "", transaction[2], date.today().isoformat())

    summary = database.calculate_summary(database.get_all_transactions())
    expected_income = sum(t[0] for t in transactions if t[1] == "INCOME")
    expected_expenses = sum(t[0] for t in transactions if t[1] == "EXPENSE")

    assert round(expected_income, 2) == round(summary[0], 2)
    assert round(expected_expenses, 2) == round(summary[1], 2)
    assert round(expected_income - expected_expenses, 2) == round(summary[2], 2)