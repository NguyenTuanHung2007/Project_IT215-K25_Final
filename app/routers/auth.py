from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.core.security import create_access_token, create_refresh_token
from app.schemas.auth_schema import (
	LoginRequest,
	RefreshTokenRequest,
	RegisterRequest,
	TokenResponse,
	UserResponse,
)
from app.services.auth_service import authenticate_user, refresh_user_tokens, register_user


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
	return register_user(db, data)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
	user = authenticate_user(db, data)
	access_token = create_access_token(
		subject=str(user.id),
		email=user.email,
		role=user.role,
	)
	refresh_token = create_refresh_token(
		subject=str(user.id),
		email=user.email,
		role=user.role,
	)
	return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenResponse)
def refresh(data: RefreshTokenRequest, db: Session = Depends(get_db)):
	user = refresh_user_tokens(db, data.refresh_token)
	return TokenResponse(
		access_token=create_access_token(
			subject=str(user.id), email=user.email, role=user.role
		),
		refresh_token=create_refresh_token(
			subject=str(user.id), email=user.email, role=user.role
		),
	)
