from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.exceptions import (
	ConflictException,
	ForbiddenException,
	UnauthorizedException,
)
from app.core.security import decode_refresh_token
from app.models.user import User
from app.schemas.auth_schema import LoginRequest, RegisterRequest
from app.utils.password_service import hash_password, verify_password


def register_user(db: Session, data: RegisterRequest) -> User:
	normalized_email = str(data.email).strip().lower()

	existing_user = db.scalar(select(User).where(User.email == normalized_email))
	if existing_user is not None:
		raise ConflictException("Email đã được đăng kí")

	user = User(
		email=normalized_email,
		password_hash=hash_password(data.password),
		full_name=data.full_name.strip(),
		role="USER",
		is_active=True,
		created_at=datetime.now(timezone.utc),
	)
	db.add(user)

	try:
		db.commit()
	except IntegrityError:
		db.rollback()
		raise ConflictException("Email đã được đăng kí") from None

	db.refresh(user)
	return user


def authenticate_user(db: Session, data: LoginRequest) -> User:
	normalized_email = str(data.email).strip().lower()
	user = db.scalar(select(User).where(User.email == normalized_email))

	if user is None or not verify_password(data.password, user.password_hash):
		raise UnauthorizedException()
	if not user.is_active:
		raise ForbiddenException("Tài khoản đã bị vô hiệu hóa")

	return user


def refresh_user_tokens(db: Session, refresh_token: str) -> User:
	payload = decode_refresh_token(refresh_token)
	user_id = payload.get("sub") if payload else None
	if user_id is None:
		raise UnauthorizedException("Refresh token không hợp lệ hoặc đã hết hạn")

	try:
		user_id = int(user_id)
	except (TypeError, ValueError):
		raise UnauthorizedException("Thông tin người dùng trong token không hợp lệ") from None

	user = db.scalar(select(User).where(User.id == user_id))
	if user is None:
		raise UnauthorizedException("Tài khoản không tồn tại")
	if not user.is_active:
		raise ForbiddenException("Tài khoản đã bị vô hiệu hóa")

	return user
