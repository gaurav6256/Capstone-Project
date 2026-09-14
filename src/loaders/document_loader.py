from pathlib import Path
from docx import Document
from pypdf import PdfReader
from src.logger import logger

SUPPORTED_EXTENSIONS = {".txt", ".pdf", ".docx"}

class DocumentLoader:
    @staticmethod
    def extract_text(file_path: Path) -> str:
        extension = file_path.suffix.lower()
        try:
            if extension == ".txt":
                return file_path.read_text(encoding="utf-8")
            if extension == ".pdf":
                reader = PdfReader(str(file_path))
                return "\n".join(page.extract_text() or "" for page in reader.pages)
            if extension == ".docx":
                document = Document(str(file_path))
                return "\n".join(p.text for p in document.paragraphs if p.text.strip())
            raise ValueError(f"Unsupported file format: {extension}")
        except Exception as error:
            logger.exception("Failed to process %s", file_path.name)
            raise RuntimeError(f"Could not extract text from {file_path.name}: {error}") from error
