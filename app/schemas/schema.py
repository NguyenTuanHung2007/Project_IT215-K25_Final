from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ORMBaseSchema(BaseModel):
	model_config = ConfigDict(from_attributes=True)


class UserBase(ORMBaseSchema):
	email: str
	full_name: str
	role: str = "USER"
	is_active: bool = True


class UserCreate(UserBase):
	password: str


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
	name: str
	description: Optional[str] = None
	owner_id: Optional[int] = None


class ConstructionSiteCreate(ConstructionSiteBase):
	pass


class ConstructionSiteUpdate(ORMBaseSchema):
	name: Optional[str] = None
	description: Optional[str] = None
	owner_id: Optional[int] = None


class ConstructionSiteResponse(ConstructionSiteBase):
	id: int
	created_at: datetime


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
	title: Optional[str] = None
	description: Optional[str] = None
	assignee_id: Optional[int] = None
	status: Optional[str] = None
	priority: Optional[str] = None
	due_date: Optional[datetime] = None


class WorkItemResponse(WorkItemBase):
	id: int
	created_at: datetime
