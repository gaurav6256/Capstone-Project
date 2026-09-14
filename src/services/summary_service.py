from langchain_core.prompts import ChatPromptTemplate
from src.schemas import CaseSummary, ComplaintData

class SummaryService:
    def __init__(self, llm):
        self.structured_llm = llm.with_structured_output(CaseSummary)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", '''Generate a concise internal management summary using only the provided case information.
Do not invent facts. Include case overview, key issue, action taken, current status, and recommended next action.
If information is unavailable, explicitly state that it was not provided.'''),
            ("human", "Case data:\n{case_data}")
        ])
        self.chain = self.prompt | self.structured_llm

    def generate(self, complaint: ComplaintData) -> CaseSummary:
        return self.chain.invoke({"case_data": complaint.model_dump_json(indent=2)})
