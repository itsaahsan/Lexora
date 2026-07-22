from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class DocumentResponse(BaseModel):
    id: Any
    filename: str
    file_type: str
    file_size: int
    status: str
    chunk_count: int
    created_at: datetime

    class Config:
        from_attributes = True

    def model_dump(self, **kwargs):
        d = super().model_dump(**kwargs)
        d["id"] = str(d["id"])
        return d


class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]
    total: int
