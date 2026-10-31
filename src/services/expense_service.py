import sqlite3
from pathlib import Path

from src.database.repository import add_expense
from src.models.expense import Expense
from src.ocr.parser import parse_receipt
from src.ocr.reader import read_text


def process_receipt(
    image_path: str | Path,
    database_connection: sqlite3.Connection,
    language: str = "tur+eng",
) -> Expense:
    raw_text = read_text(image_path, language=language)
    expense = parse_receipt(raw_text)
    add_expense(database_connection, expense)
    return expense
