from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class Source(BaseModel):
    document_id: str
    filename: str
    chunk_text: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
    conversation_id: str


class MessageResponse(BaseModel):
    id: Any
    role: str
    content: str
    sources: list[dict]
    created_at: datetime

    class Config:
        from_attributes = True

    def model_dump(self, **kwargs):
        d = super().model_dump(**kwargs)
        d["id"] = str(d["id"])
        return d


class ConversationResponse(BaseModel):
    id: Any
    title: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    def model_dump(self, **kwargs):
        d = super().model_dump(**kwargs)
        d["id"] = str(d["id"])
        return d


class ConversationListResponse(BaseModel):
    conversations: list[ConversationResponse]
    total: int
