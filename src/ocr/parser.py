import re
from datetime import date
from decimal import Decimal, InvalidOperation

from src.models.expense import Expense


class ReceiptParseError(ValueError):
    """Raised when required expense fields cannot be extracted."""


DATE_PATTERNS = (
    re.compile(r"\b(?P<day>\d{1,2})[./-](?P<month>\d{1,2})[./-](?P<year>\d{2,4})\b"),
    re.compile(r"\b(?P<year>20\d{2})[./-](?P<month>\d{1,2})[./-](?P<day>\d{1,2})\b"),
)

AMOUNT_PATTERN = re.compile(
    r"(?i)(?:genel\s+toplam|toplam|total|tutar|ödenecek)\D{0,15}"
    r"(?P<amount>\d{1,3}(?:[.\s]\d{3})*(?:,\d{2})|\d+(?:[.,]\d{2}))"
)

CATEGORY_KEYWORDS = {
    "Gıda": ("market", "gıda", "restoran", "restaurant", "cafe", "kasap", "manav"),
    "Ulaşım": ("akaryakıt", "benzin", "petrol", "otopark", "taksi", "metro", "otobüs"),
    "Sağlık": ("eczane", "hastane", "medikal", "klinik"),
    "Giyim": ("giyim", "tekstil", "moda", "ayakkabı", "kıyafet"),
    "Faturalar": ("elektrik", "su faturası", "internet", "telefon", "doğalgaz"),
}


def parse_receipt(text: str) -> Expense:
    if not text.strip():
        raise ReceiptParseError("Fiş metni boş olamaz.")

    expense_date = _extract_date(text)
    total_amount = _extract_total(text)
    category = _infer_category(text)
    return Expense(expense_date, total_amount, category, text)


def _extract_date(text: str) -> date:
    for pattern in DATE_PATTERNS:
        match = pattern.search(text)
        if not match:
            continue
        values = {key: int(value) for key, value in match.groupdict().items()}
        year = values["year"] + 2000 if values["year"] < 100 else values["year"]
        try:
            return date(year, values["month"], values["day"])
        except ValueError:
            continue
    raise ReceiptParseError("Fişte tarih bulunamadı.")


def _extract_total(text: str) -> Decimal:
    match = AMOUNT_PATTERN.search(text)
    if not match:
        raise ReceiptParseError("Fişte toplam tutar bulunamadı.")

    normalized = match.group("amount").replace(" ", "").replace(".", "").replace(",", ".")
    try:
        return Decimal(normalized).quantize(Decimal("0.01"))
    except InvalidOperation as error:
        raise ReceiptParseError("Fişteki toplam tutar geçersiz.") from error


def _infer_category(text: str) -> str:
    normalized = text.casefold()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            return category
    return "Diğer"
