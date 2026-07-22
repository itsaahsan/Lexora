from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.document import Document
from app.models.conversation import Conversation, Message
from app.schemas.analytics import AnalyticsOverview, DocumentAnalytics
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/overview", response_model=AnalyticsOverview)
def get_overview(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    total_docs = db.query(Document).filter(Document.user_id == current_user.id).count()
    total_convos = db.query(Conversation).filter(Conversation.user_id == current_user.id).count()

    convo_ids = [c.id for c in db.query(Conversation.id).filter(Conversation.user_id == current_user.id).all()]
    total_messages = db.query(Message).filter(Message.conversation_id.in_(convo_ids)).count() if convo_ids else 0

    total_chunks = 0
    docs = db.query(Document).filter(Document.user_id == current_user.id).all()
    for doc in docs:
        total_chunks += doc.chunk_count

    return AnalyticsOverview(
        total_documents=total_docs,
        total_conversations=total_convos,
        total_messages=total_messages,
        total_chunks=total_chunks,
    )


@router.get("/documents", response_model=DocumentAnalytics)
def get_document_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    docs = db.query(Document).filter(Document.user_id == current_user.id).all()
    by_type = {}
    by_status = {}
    for doc in docs:
        by_type[doc.file_type] = by_type.get(doc.file_type, 0) + 1
        by_status[doc.status] = by_status.get(doc.status, 0) + 1
    return DocumentAnalytics(documents_by_type=by_type, documents_by_status=by_status)
