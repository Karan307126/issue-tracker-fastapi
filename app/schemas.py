from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional

class IssueStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    closed = "closed"

class IssuePriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class IssueCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=1, max_length=500)
    status: IssueStatus = Field(default=IssueStatus.open)
    priority: IssuePriority = Field(default=IssuePriority.medium)

class IssueUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    status: Optional[IssueStatus] = None
    priority: Optional[IssuePriority] = None

class IssueOutput(BaseModel):
    id: str
    title: str
    description: str
    status: IssueStatus
    priority: IssuePriority