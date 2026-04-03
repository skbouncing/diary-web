from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DiaryEntryCreate(BaseModel):
    title:   str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    mood:    str = Field(default="보통")

class DiaryEntryUpdate(BaseModel):
    title:   Optional[str] = Field(None, max_length=200)
    content: Optional[str] = None
    mood:    Optional[str] = None

class DiaryEntryResponse(BaseModel):
    id:         int
    title:      str
    content:    str
    mood:       str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True