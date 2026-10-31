from datetime import date
from decimal import Decimal

from src.database.connection import get_connection, initialize_database
from src.database.repository import add_expense, list_expenses
from src.models.expense import Expense


def test_expense_can_be_saved_and_listed(tmp_path) -> None:
    connection = get_connection(tmp_path / "test.sqlite")
    initialize_database(connection)
    expected = Expense(date(2026, 10, 31), Decimal("42.50"), "Gıda", "MARKET")

    expense_id = add_expense(connection, expected)
    expenses = list_expenses(connection)
    connection.close()

    assert expense_id == 1
    assert expenses == [expected]
