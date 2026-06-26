from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.conversation import Conversation, Message
from app.schemas.chat import (
    ChatRequest, ChatResponse, Source,
    MessageResponse, ConversationResponse, ConversationListResponse,
)
from app.core.dependencies import get_current_user
from app.services.rag_service import retrieve_and_generate

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if request.conversation_id:
        conversation = db.query(Conversation).filter(
            Conversation.id == request.conversation_id,
            Conversation.user_id == current_user.id,
        ).first()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = Conversation(user_id=current_user.id, title=request.message[:50])
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    user_msg = Message(
        conversation_id=conversation.id,
        role="user",
        content=request.message,
    )
    db.add(user_msg)
    db.commit()

    result = retrieve_and_generate(request.message, current_user.id)

    assistant_msg = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=result["answer"],
        sources=[s.model_dump() for s in result["sources"]],
    )
    db.add(assistant_msg)
    db.commit()

    return ChatResponse(
        answer=result["answer"],
        sources=result["sources"],
        conversation_id=str(conversation.id),
    )


@router.get("/conversations", response_model=ConversationListResponse)
def list_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    convos = db.query(Conversation).filter(
        Conversation.user_id == current_user.id
    ).order_by(Conversation.updated_at.desc()).all()
    return ConversationListResponse(
        conversations=[ConversationResponse.model_validate(c) for c in convos],
        total=len(convos),
    )


@router.get("/conversations/{conv_id}/messages", response_model=list[MessageResponse])
def get_conversation_messages(
    conv_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conv = db.query(Conversation).filter(
        Conversation.id == conv_id,
        Conversation.user_id == current_user.id,
    ).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    messages = db.query(Message).filter(
        Message.conversation_id == conv_id
    ).order_by(Message.created_at).all()
    return [MessageResponse.model_validate(m) for m in messages]


@router.delete("/conversations/{conv_id}")
def delete_conversation(
    conv_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conv = db.query(Conversation).filter(
        Conversation.id == conv_id,
        Conversation.user_id == current_user.id,
    ).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    db.query(Message).filter(Message.conversation_id == conv_id).delete()
    db.delete(conv)
    db.commit()
    return {"detail": "Conversation deleted"}
