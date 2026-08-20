from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.dependencies import get_current_user, get_db, require_admin
from app.models.user import User
from app.schemas.auth_schema import UserResponse
from app.services.user_service import list_users


users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
	return current_user

@users_router.get("", response_model=list[UserResponse])
def get_users(search: str | None = Query(default=None),is_active: bool | None = Query(default=None), admin_user: User = Depends(require_admin),db: Session = Depends(get_db),):
	return list_users(db, search=search, is_active=is_active)
