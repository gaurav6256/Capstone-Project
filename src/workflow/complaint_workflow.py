import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from src.logger import logger
from src.loaders.document_loader import DocumentLoader

class ComplaintWorkflow:
    def __init__(self, extraction_service, email_service, summary_service,
                 structured_output_dir: Path, email_output_dir: Path, summary_output_dir: Path):
        self.extraction_service = extraction_service
        self.email_service = email_service
        self.summary_service = summary_service
        self.structured_output_dir = structured_output_dir
        self.email_output_dir = email_output_dir
        self.summary_output_dir = summary_output_dir

    def process_document(self, file_path: Path) -> dict:
        logger.info("Processing document: %s", file_path.name)
        try:
            document_text = DocumentLoader.extract_text(file_path)
            if not document_text.strip():
                raise ValueError("Document contains no extractable text.")

            complaint_data = self.extraction_service.extract(document_text)

            # Independent downstream AI tasks run in parallel.
            with ThreadPoolExecutor(max_workers=2) as executor:
                email_future = executor.submit(self.email_service.generate, complaint_data)
                summary_future = executor.submit(self.summary_service.generate, complaint_data)
                customer_email = email_future.result()
                case_summary = summary_future.result()

            self._save_structured_data(file_path, complaint_data)
            self._save_customer_email(file_path, customer_email)
            self._save_case_summary(file_path, case_summary)

            return {"file_name": file_path.name, "status": "Success", **complaint_data.model_dump()}
        except Exception as error:
            logger.exception("Failed to process document: %s", file_path.name)
            return {"file_name": file_path.name, "status": "Failed", "error": str(error)}

    def _save_structured_data(self, file_path, complaint_data):
        path = self.structured_output_dir / f"{file_path.stem}.json"
        path.write_text(json.dumps(complaint_data.model_dump(), indent=2, ensure_ascii=False), encoding="utf-8")

    def _save_customer_email(self, file_path, customer_email):
        path = self.email_output_dir / f"{file_path.stem}_email.txt"
        path.write_text(customer_email, encoding="utf-8")

    def _save_case_summary(self, file_path, case_summary):
        path = self.summary_output_dir / f"{file_path.stem}_summary.json"
        path.write_text(json.dumps(case_summary.model_dump(), indent=2, ensure_ascii=False), encoding="utf-8")
