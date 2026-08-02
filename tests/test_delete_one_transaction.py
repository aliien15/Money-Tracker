from spend.database import Database
from datetime import date
from hypothesis import given, strategies as st
import random

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
def test_delete_one_transaction(transactions):
    database = Database(":memory:")

    for transaction in transactions:
        database.insert_transaction(transaction[0], transaction[1], "", transaction[2], date.today().isoformat())

    all_transactions = database.get_all_transactions()
    id_to_delete = random.choice(all_transactions)[0]

    database.delete_transaction(id_to_delete)
    all_new_transactions = database.get_all_transactions()
    assert len(all_new_transactions) == len(all_transactions) - 1
    assert id_to_delete not in [transaction[0] for transaction in all_new_transactions]