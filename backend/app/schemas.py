from pydantic import BaseModel, Field
from typing import List

class ReportCreate(BaseModel):
    title: str = Field(min_length=1)
    content: str = Field(min_length=1)
    tags: List[str] = Field(default_factory=list)
    date: str = Field(min_length=1)

class ReportOut(ReportCreate):
    id: int