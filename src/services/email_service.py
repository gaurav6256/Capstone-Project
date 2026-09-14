from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from src.schemas import ComplaintData

class EmailService:
    def __init__(self, llm):
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", '''You are a professional customer support representative.
Generate a professional response email using only the supplied case data.
Do not invent resolutions, refunds, timelines, promises, policies, or actions.
Summarize the issue and mention the known resolution or current status.
Return only the email content.'''),
            ("human", '''Customer Name: {customer_name}
Issue Description: {issue_description}
Resolution Provided: {resolution_provided}
Case Status: {case_status}
Escalation Required: {escalation_required}''')
        ])
        self.chain = self.prompt | llm | StrOutputParser()

    def generate(self, complaint: ComplaintData) -> str:
        return self.chain.invoke({
            "customer_name": complaint.customer_name or "Customer",
            "issue_description": complaint.issue_description or "Not specified",
            "resolution_provided": complaint.resolution_provided or "No resolution information is available.",
            "case_status": complaint.overall_case_status or "Status currently unavailable.",
            "escalation_required": complaint.escalation_required,
        })
