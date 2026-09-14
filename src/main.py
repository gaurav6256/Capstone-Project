import warnings

warnings.filterwarnings(
    "ignore",
    message=".*uses fixed sampling defaults.*"
)

warnings.filterwarnings(
    "ignore",
    message=".*Direct use of automatic function calling.*"
)
from src.config import (
    CASE_SUMMARY_DIR, CUSTOMER_EMAIL_DIR, DATA_DIR, OUTPUT_DIR,
    STRUCTURED_DATA_DIR, validate_config
)
from src.logger import logger
from src.services.llm_service import get_llm
from src.services.extraction_service import ExtractionService
from src.services.email_service import EmailService
from src.services.summary_service import SummaryService
from src.utils.file_utils import ensure_directories, get_supported_files
from src.utils.report_generator import ReportGenerator
from src.workflow.complaint_workflow import ComplaintWorkflow

def main():
    logger.info("Starting AI Complaint & Case Processing System")
    try:
        validate_config()
        ensure_directories([
            DATA_DIR, OUTPUT_DIR, STRUCTURED_DATA_DIR,
            CUSTOMER_EMAIL_DIR, CASE_SUMMARY_DIR
        ])

        files = get_supported_files(DATA_DIR)
        if not files:
            print("No supported documents found in data/.")
            return

        print(f"Found {len(files)} document(s).")
        llm = get_llm()
        workflow = ComplaintWorkflow(
            ExtractionService(llm),
            EmailService(llm),
            SummaryService(llm),
            STRUCTURED_DATA_DIR,
            CUSTOMER_EMAIL_DIR,
            CASE_SUMMARY_DIR,
        )

        results = [workflow.process_document(file_path) for file_path in files]
        report_path = ReportGenerator.generate(results, OUTPUT_DIR)
        print(f"Processing completed. Final report: {report_path}")
    except Exception as error:
        logger.exception("Application terminated due to an error.")
        print(f"Application failed: {error}")

if __name__ == "__main__":
    main()
