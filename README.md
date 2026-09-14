# AI-Powered Customer Complaint & Case Processing System

## Problem Statement
This application automatically processes a batch of customer business documents and performs:
1. Structured information extraction
2. Professional customer response generation
3. Internal management case-summary generation

## Architecture

```text
Documents (.txt / .pdf / .docx)
            |
            v
     Document Ingestion
            |
            v
       Text Extraction
            |
            v
  LLM Structured Extraction
       (Pydantic Schema)
            |
       +----+----+
       |         |
       v         v
Customer Email  Case Summary
       |         |
       +----+----+
            |
            v
 Individual Outputs + final_report.csv
```

The email and case-summary generation steps are executed in parallel after structured extraction.

## Technology Stack
- Python
- LangChain
- Google Gemini API
- Pydantic
- PyPDF
- python-docx
- pandas
- python-dotenv

## Project Structure
```text
src/        Application source code
data/       Input documents
output/     Generated results
logs/       Application logs
```

## Setup

### 1. Create a virtual environment
```bash
python -m venv venv
```

### 2. Activate it
Windows:
```bash
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
In `.env` add:
```env
GOOGLE_API_KEY=your_api_key
```

### 5. Run
```bash
python -m src.main
```

## Input
Place `.txt`, `.pdf`, or `.docx` complaint documents in `data/`.

## Output
The application generates:
- `output/structured_data/*.json`
- `output/customer_emails/*.txt`
- `output/case_summaries/*.json`
- `output/final_report.csv`

## Key Design Decisions
- Pydantic schemas validate structured extraction.
- The workflow separates extraction, email generation, and case summarization.
- Independent downstream AI tasks execute in parallel.
- File-level errors are handled without stopping the complete batch.
- Configuration and API keys are separated from source code.
- Logging records processing activity and failures.

## Limitations
- Scanned PDFs without extractable text are not currently OCR-processed.
- Very large documents may require chunking in a future version.
- Generated outputs depend on the information available in the source document and LLM behavior.
