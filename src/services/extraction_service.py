from langchain_core.prompts import ChatPromptTemplate
from src.schemas import ComplaintData

class ExtractionService:
    def __init__(self, llm):
        self.structured_llm = llm.with_structured_output(ComplaintData)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", '''You process customer business documents. Extract only information present in the document.
Rules:
1. Do not invent information.
2. Use null for unavailable text fields.
3. Set Yes/No fields based only on the document.
4. Keep the output factual and concise.
Follow the schema exactly.'''),
            ("human", "Document content:\n{document_text}")
        ])
        self.chain = self.prompt | self.structured_llm

    def extract(self, document_text: str) -> ComplaintData:
        return self.chain.invoke({"document_text": document_text})
