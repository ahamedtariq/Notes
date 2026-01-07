from pydantic import BaseModel,Field
from typing import Optional 



class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)
    summary: Optional[str] = Field(None)

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = Field(..., min_length=1, max_length=100, description="Note title")
    content:Optional[str] = Field(..., min_length=1, description="Note content")
    summary: Optional[str] = Field(None, description="Note summary")