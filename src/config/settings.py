from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATA_DIR / "expenses.sqlite"
WINDOWS_TESSERACT = Path("C:/Program Files/Tesseract-OCR/tesseract.exe")
TESSERACT_COMMAND = (
    str(WINDOWS_TESSERACT)
    if WINDOWS_TESSERACT.exists()
    else "tesseract"
)
