from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenException, UnauthorizedException
from app.core.security import decode_access_token
from app.dependencies.database import get_db
from app.models.user import User

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],db: Session = Depends(get_db),) -> User:
	if credentials is None:
		raise UnauthorizedException("Yêu cầu đăng nhập")

	payload = decode_access_token(credentials.credentials)
	user_id = payload.get("sub") if payload else None
	if user_id is None:
		raise UnauthorizedException("Token không hợp lệ hoặc đã hết hạn")

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


def require_admin(current_user: User = Depends(get_current_user)) -> User:
	if (current_user.role or "").upper() != "ADMIN":
		raise ForbiddenException("Chỉ quản trị viên mới có quyền thực hiện thao tác này")
	return current_user
