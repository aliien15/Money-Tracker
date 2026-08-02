from spend.database import Database
from datetime import date
from hypothesis import given, strategies as st

@given(
    amount=st.floats(min_value=0.01, max_value=500.0),
    transaction_type=st.sampled_from(["INCOME", "EXPENSE"]),
    description=st.text(min_size=1, max_size=20)
)
def test_insert_and_retrieve_transaction(amount, transaction_type, description):
    database = Database(":memory:")
    database.insert_transaction(amount, transaction_type, "", description, date.today().isoformat())
    result = database.get_all_transactions()

    assert len(result) == 1