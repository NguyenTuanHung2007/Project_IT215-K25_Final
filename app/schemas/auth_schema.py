from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class ORMBaseSchema(BaseModel):
	model_config = ConfigDict(from_attributes=True)


class UserBase(ORMBaseSchema):
	email: EmailStr
	full_name: str = Field(min_length=1, max_length=50)
	role: str = "USER"
	is_active: bool = True


class UserCreate(UserBase):
	password: str = Field(min_length=8, max_length=128)


class RegisterRequest(ORMBaseSchema):
	email: EmailStr
	full_name: str = Field(min_length=1, max_length=50)
	password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
	email: EmailStr
	password: str = Field(min_length=1, max_length=128)


class TokenResponse(BaseModel):
	access_token: str
	refresh_token: str
	token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
	refresh_token: str = Field(min_length=1)


class UserUpdate(ORMBaseSchema):
	email: Optional[str] = None
	full_name: Optional[str] = None
	role: Optional[str] = None
	is_active: Optional[bool] = None
	password: Optional[str] = None


class UserResponse(UserBase):
	id: int
	created_at: datetime


class ConstructionSiteBase(ORMBaseSchema):
	name: str = Field(min_length=1, max_length=50)
	description: Optional[str] = None
	owner_id: Optional[int] = None

	@field_validator("name")
	@classmethod
	def validate_name(cls, value: str) -> str:
		if not value.strip():
			raise ValueError("Tên công trình không được để trống")
		return value


class ConstructionSiteCreate(ORMBaseSchema):
	name: str = Field(min_length=1, max_length=50)
	description: Optional[str] = None

	@field_validator("name")
	@classmethod
	def validate_name(cls, value: str) -> str:
		if not value.strip():
			raise ValueError("Tên công trình không được để trống")
		return value


class ConstructionSiteUpdate(ORMBaseSchema):
	name: Optional[str] = Field(default=None, min_length=1, max_length=50)
	description: Optional[str] = None
	owner_id: Optional[int] = None

	@field_validator("name")
	@classmethod
	def validate_name(cls, value: str | None) -> str | None:
		if value is not None and not value.strip():
			raise ValueError("Tên công trình không được để trống")
		return value


class ConstructionSiteResponse(ConstructionSiteBase):
	id: int
	created_at: datetime
	deleted_at: Optional[datetime] = None


class SiteMemberBase(ORMBaseSchema):
	site_id: int
	user_id: int
	role: str


class SiteMemberCreate(SiteMemberBase):
	joined_at: datetime


class SiteMemberUpdate(ORMBaseSchema):
	role: Optional[str] = None


class SiteMemberResponse(SiteMemberBase):
	joined_at: datetime


class WorkItemBase(ORMBaseSchema):
	site_id: int
	title: str
	description: Optional[str] = None
	assignee_id: Optional[int] = None
	status: str
	priority: str
	due_date: Optional[datetime] = None


class WorkItemCreate(WorkItemBase):
	pass

class WorkItemUpdate(ORMBaseSchema):
	site_id: Optional[int] = None
	title: Optional[str] = Field(default=None, min_length=1, max_length=255)
	description: Optional[str] = None
	assignee_id: Optional[int] = None
	status: Optional[str] = Field(default=None, min_length=1, max_length=50)
	priority: Optional[str] = Field(default=None, min_length=1, max_length=50)
	due_date: Optional[datetime] = None


class WorkItemResponse(WorkItemBase):
	id: int
	created_at: datetime
