from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from jwt.exceptions import PyJWTError

from app.core.config import settings


def create_token(subject: str, email: str, role: str, token_type: str, expires_minutes: int) -> str:
	expires_at = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
	payload: dict[str, Any] = {
		"sub": subject,
		"email": email,
		"role": role,
		"type": token_type,
		"exp": expires_at,
	}
	return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def create_access_token(subject: str, email: str, role: str) -> str:
	return create_token(
		subject, email, role, "access", settings.access_token_expire_minutes
	)


def create_refresh_token(subject: str, email: str, role: str) -> str:
	return create_token(
		subject, email, role, "refresh", settings.refresh_token_expire_minutes
	)


def decode_access_token(token: str) -> dict[str, Any] | None:
	try:
		payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
		return payload if payload.get("type") == "access" else None
	except PyJWTError:
		return None


def decode_refresh_token(token: str) -> dict[str, Any] | None:
	try:
		payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
		return payload if payload.get("type") == "refresh" else None
	except PyJWTError:
		return None
