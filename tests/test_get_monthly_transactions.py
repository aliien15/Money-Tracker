from spend.database import Database
from datetime import date
from hypothesis import given, strategies as st

@given(
    transactions=st.lists(
        st.tuples(
            st.floats(min_value=0.01, max_value=500.0),
            st.sampled_from(["INCOME", "EXPENSE"]),
            st.text(min_size=1, max_size=20),
            st.sampled_from(["2026-08-02", "2026-08-15", "2026-08-27", "2026-07-02", "2027-08-02", "2026-11-05", "2027-04-015"])
        ),
        min_size=1,
        max_size=20
    )
)
def test_get_monthly_transactions(transactions):
    database = Database(":memory:")
    
    for transaction in transactions:
        database.insert_transaction(transaction[0], transaction[1], "", transaction[2], transaction[3])

    monthly_transactions = database.get_monthly_transactions("2026-08")

    assert (len(monthly_transactions)) == len([t for t in transactions if t[3].startswith("2026-08")])
    assert all(row[5].startswith("2026-08") for row in monthly_transactions)