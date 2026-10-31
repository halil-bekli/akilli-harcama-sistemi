from pathlib import Path

from PIL import Image
import pytesseract

from src.config.settings import TESSERACT_COMMAND


class OCRReaderError(RuntimeError):
    """Raised when an image cannot be processed by the OCR engine."""


def read_text(image_path: str | Path, language: str = "tur+eng") -> str:
    path = Path(image_path)
    if not path.is_file():
        raise OCRReaderError(f"Fiş görseli bulunamadı: {path}")

    try:
        image = Image.open(path)
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_COMMAND
        text = pytesseract.image_to_string(image, lang=language)
    except (OSError, pytesseract.TesseractError) as error:
        raise OCRReaderError(f"OCR işlemi başarısız oldu: {error}") from error

    if not text.strip():
        raise OCRReaderError("OCR sonucunda okunabilir metin bulunamadı.")
    return text
