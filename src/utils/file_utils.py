from pathlib import Path
from src.loaders.document_loader import SUPPORTED_EXTENSIONS

def ensure_directories(directories):
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

def get_supported_files(data_directory: Path):
    if not data_directory.exists():
        return []
    return sorted(
        p for p in data_directory.iterdir()
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
    )
