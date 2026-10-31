import sqlite3
from datetime import date
from decimal import Decimal

from src.models.expense import Expense


def add_expense(connection: sqlite3.Connection, expense: Expense) -> int:
    cursor = connection.execute(
        """
        INSERT INTO expenses (expense_date, total_amount, category, raw_text)
        VALUES (?, ?, ?, ?)
        """,
        (
            expense.expense_date.isoformat(),
            str(expense.total_amount),
            expense.category,
            expense.raw_text,
        ),
    )
    connection.commit()
    return int(cursor.lastrowid)


def list_expenses(connection: sqlite3.Connection) -> list[Expense]:
    rows = connection.execute(
        """
        SELECT expense_date, total_amount, category, raw_text
        FROM expenses
        ORDER BY expense_date DESC, id DESC
        """
    ).fetchall()
    return [
        Expense(
            expense_date=date.fromisoformat(row["expense_date"]),
            total_amount=Decimal(str(row["total_amount"])),
            category=row["category"],
            raw_text=row["raw_text"],
        )
        for row in rows
    ]
