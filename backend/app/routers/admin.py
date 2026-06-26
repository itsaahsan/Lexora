from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.document import Document
from app.models.conversation import Conversation
from app.schemas.user import UserResponse
from app.core.dependencies import get_current_admin_user

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=list[UserResponse])
def list_users(
    admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    users = db.query(User).all()
    return [UserResponse.model_validate(u) for u in users]


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: str,
    role: str = None,
    is_active: bool = None,
    admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if role is not None:
        user.role = role
    if is_active is not None:
        user.is_active = is_active
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)


@router.get("/stats")
def get_stats(
    admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    return {
        "total_users": db.query(User).count(),
        "total_documents": db.query(Document).count(),
        "total_conversations": db.query(Conversation).count(),
        "active_users": db.query(User).filter(User.is_active == True).count(),
    }
