from pydantic import BaseModel
from typing import Optional

from enum import Enum

class StatusOptions(str, Enum):
    applied = "Applied"
    interview = "Interview"
    offered = "Offered"
    rejected = "Rejected"
    accepted = "Accepted"

class JobApplicationCreate(BaseModel):
    company: str
    job_title: str
    job_posting_link: str
    applied: Optional[bool] = False
    application_date: Optional[str] = None
    referred: Optional[bool] = False
    status: Optional[str] = ""
    notes: Optional[str] = ""