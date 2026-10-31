from datetime import date
from decimal import Decimal

from src.ocr.parser import parse_receipt


def test_parse_receipt_extracts_expense_fields() -> None:
    expense = parse_receipt(
        "MIGROS MARKET\nTarih: 31.10.2026\nGENEL TOPLAM: 1.234,56 TL"
    )

    assert expense.expense_date == date(2026, 10, 31)
    assert expense.total_amount == Decimal("1234.56")
    assert expense.category == "Gıda"
