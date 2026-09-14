import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0"))

DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
STRUCTURED_DATA_DIR = OUTPUT_DIR / "structured_data"
CUSTOMER_EMAIL_DIR = OUTPUT_DIR / "customer_emails"
CASE_SUMMARY_DIR = OUTPUT_DIR / "case_summaries"
LOG_DIR = BASE_DIR / "logs"

def validate_config():
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is missing. Add it to your .env file.")
