from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class Expense:
    expense_date: date
    total_amount: Decimal
    category: str
    raw_text: str

