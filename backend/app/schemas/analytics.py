from pydantic import BaseModel


class AnalyticsOverview(BaseModel):
    total_documents: int
    total_conversations: int
    total_messages: int
    total_chunks: int


class DocumentAnalytics(BaseModel):
    documents_by_type: dict[str, int]
    documents_by_status: dict[str, int]
