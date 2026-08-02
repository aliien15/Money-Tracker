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
def test_delete_all_transactions(transactions):
    database = Database(":memory:")

    for transaction in transactions:
        database.insert_transaction(transaction[0], transaction[1], "", transaction[2], date.today().isoformat())

    entries_deleted = database.delete_all()
    assert entries_deleted == len(transactions)
    assert len(database.get_all_transactions()) == 0