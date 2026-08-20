import time
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.exceptions import (
	ConflictException,
	ForbiddenException,
	TooManyRequestsException,
	UnauthorizedException,
)
from app.core.security import decode_refresh_token
from app.models.user import User
from app.schemas.auth_schema import LoginRequest, RegisterRequest
from app.utils.password_service import hash_password, verify_password


failed_login_attempts: dict[str, list[float]] = {}
login_lockouts: dict[str, float] = {}


def check_login_rate_limit(login_key: str) -> None:
	now = time.monotonic()
	lockout_until = login_lockouts.get(login_key, 0)
	if now < lockout_until:
		remaining_seconds = int(lockout_until - now) + 1
		raise TooManyRequestsException(
			f"Tài khoản đăng nhập tạm thời bị khóa. Vui lòng thử lại sau "
			f"{remaining_seconds} giây"
		)
	login_lockouts.pop(login_key, None)
	attempts = [
		attempt
		for attempt in failed_login_attempts.get(login_key, [])
		if now - attempt < settings.login_window_seconds
	]
	failed_login_attempts[login_key] = attempts
	if len(attempts) >= settings.login_max_attempts:
		raise TooManyRequestsException(
			f"Bạn đã đăng nhập sai quá nhiều lần. Vui lòng thử lại sau "
			f"{settings.login_lockout_seconds // 60} phút"
		)


def record_failed_login(login_key: str) -> None:
	attempts = failed_login_attempts.setdefault(login_key, [])
	attempts.append(time.monotonic())
	if len(attempts) >= settings.login_max_attempts:
		login_lockouts[login_key] = time.monotonic() + settings.login_lockout_seconds


def clear_failed_logins(login_key: str) -> None:
	failed_login_attempts.pop(login_key, None)
	login_lockouts.pop(login_key, None)


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
	check_login_rate_limit(normalized_email)
	user = db.scalar(select(User).where(User.email == normalized_email))

	if user is None or not verify_password(data.password, user.password_hash):
		record_failed_login(normalized_email)
		raise UnauthorizedException()
	if not user.is_active:
		raise ForbiddenException("Tài khoản đã bị vô hiệu hóa")

	clear_failed_logins(normalized_email)
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
