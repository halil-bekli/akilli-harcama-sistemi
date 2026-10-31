import argparse
from pathlib import Path

from src.config.settings import DATABASE_PATH, TESSERACT_COMMAND
from src.database.connection import get_connection, initialize_database
from src.services.expense_service import process_receipt


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fiş görselini OCR ile okuyup SQLite'a kaydeder."
    )
    parser.add_argument("image", type=Path, help="İşlenecek fiş/fatura görseli")
    parser.add_argument(
        "--database",
        type=Path,
        default=DATABASE_PATH,
        help=f"SQLite dosyası (varsayılan: {DATABASE_PATH})",
    )
    parser.add_argument(
        "--language",
        default="tur+eng",
        help="Tesseract dil kodu (varsayılan: tur+eng)",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if not Path(TESSERACT_COMMAND).exists() and TESSERACT_COMMAND == "tesseract":
        print(
            "Tesseract bulunamadı. Tesseract'ı kurun veya "
            "src/config/settings.py içindeki yolu güncelleyin."
        )
        return 1

    connection = get_connection(args.database)
    try:
        initialize_database(connection)
        expense = process_receipt(args.image, connection, language=args.language)
    finally:
        connection.close()

    print(f"Tarih: {expense.expense_date.isoformat()}")
    print(f"Toplam: {expense.total_amount}")
    print(f"Kategori: {expense.category}")
    print(f"Veritabanı: {args.database}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
