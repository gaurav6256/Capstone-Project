from typing import Literal, Optional
from pydantic import BaseModel, Field

class ComplaintData(BaseModel):
    customer_name: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    phone_number: Optional[str] = Field(default=None)
    complaint_category: Optional[str] = Field(default=None)
    issue_description: Optional[str] = Field(default=None)
    resolution_provided: Optional[str] = Field(default=None)
    is_complaint: Literal["Yes", "No"]
    escalation_required: Literal["Yes", "No"]
    supporting_document_available: Literal["Yes", "No"]
    overall_case_status: Optional[str] = Field(default=None)

class CaseSummary(BaseModel):
    case_overview: str
    key_issue: str
    action_taken: str
    current_status: str
    recommended_next_action: str
