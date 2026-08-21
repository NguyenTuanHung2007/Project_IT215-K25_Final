from datetime import datetime, timezone

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictException, ForbiddenException, NotFoundException
from app.models.site import ConstructionSite, SiteMember
from app.models.user import User
from app.utils.audit_logger import log_audit_event


def create_site(db: Session,current_user: User,name: str,description: str | None = None,) -> ConstructionSite:
	created_at = datetime.now(timezone.utc)
	site = ConstructionSite(
		name=name,
		description=description,
		owner_id=current_user.id,
		created_at=created_at,
	)
	db.add(site)
	db.flush()
	db.add(
		SiteMember(
			site_id=site.id,
			user_id=current_user.id,
			role="OWNER",
			joined_at=created_at,
		)
	)
	db.commit()
	db.refresh(site)
	log_audit_event(
		"CREATE_SITE",
		actor_id=current_user.id,
		site_id=site.id,
		details={"name": site.name},
	)
	return site


def list_sites(db: Session,current_user: User,search: str | None = None,) -> list[ConstructionSite]:
	member_site = select(SiteMember.site_id).where(
		SiteMember.site_id == ConstructionSite.id,
		SiteMember.user_id == current_user.id,
	).exists()
	query = select(ConstructionSite).where(ConstructionSite.deleted_at.is_(None)).order_by(ConstructionSite.id)
	query = query.where(
		or_(ConstructionSite.owner_id == current_user.id, member_site)
	)

	if search:
		search_term = search.strip()
		if search_term:
			query = query.where(ConstructionSite.name.ilike(f"%{search_term}%"))

	return list(db.scalars(query).all())


def update_site(db: Session,site_id: int,current_user: User,data: dict,) -> ConstructionSite:
	site = db.scalar(
		select(ConstructionSite).where(
			ConstructionSite.id == site_id,
			ConstructionSite.deleted_at.is_(None),
		)
	)
	if site is None:
		raise NotFoundException("Công trình không tồn tại")

	if site.owner_id != current_user.id:
		raise ForbiddenException("Chỉ chủ công trình mới có quyền sửa công trình")

	for field in ("name", "description"):
		if field in data:
			setattr(site, field, data[field])

	db.commit()
	db.refresh(site)
	log_audit_event(
		"UPDATE_SITE",
		actor_id=current_user.id,
		site_id=site.id,
		details={"fields": list(data.keys())},
	)
	return site


def delete_site(db: Session, site_id: int, current_user: User) -> None:
	site = db.scalar(
		select(ConstructionSite).where(
			ConstructionSite.id == site_id,
			ConstructionSite.deleted_at.is_(None),
		)
	)
	if site is None:
		raise NotFoundException("Công trình không tồn tại")

	if site.owner_id != current_user.id:
		raise ForbiddenException("Chỉ chủ công trình mới có quyền xóa công trình")

	site.deleted_at = datetime.now(timezone.utc)
	db.commit()
	log_audit_event(
		"DELETE_SITE",
		actor_id=current_user.id,
		site_id=site.id,
	)


def add_site_member(db: Session,site_id: int,user_id: int,current_user: User,) -> SiteMember:
	site = db.scalar(
		select(ConstructionSite).where(
			ConstructionSite.id == site_id,
			ConstructionSite.deleted_at.is_(None),
		)
	)
	if site is None:
		raise NotFoundException("Công trình không tồn tại")

	if site.owner_id != current_user.id:
		raise ForbiddenException("Chỉ chủ công trình mới có quyền thêm thành viên")

	if db.get(User, user_id) is None:
		raise NotFoundException("Người dùng không tồn tại")

	if db.scalar(
		select(SiteMember).where(
			SiteMember.site_id == site_id,
			SiteMember.user_id == user_id,
		)
	) is not None:
		raise ConflictException("Thành viên đã thuộc công trình")

	member = SiteMember(
		site_id=site_id,
		user_id=user_id,
		role="MEMBER",
		joined_at=datetime.now(timezone.utc),
	)
	db.add(member)
	db.commit()
	db.refresh(member)
	log_audit_event(
		"ADD_MEMBER",
		actor_id=current_user.id,
		site_id=site_id,
		target_user_id=user_id,
	)
	return member


def remove_site_member(db: Session,site_id: int,user_id: int,current_user: User,) -> None:
	site = db.scalar(
		select(ConstructionSite).where(
			ConstructionSite.id == site_id,
			ConstructionSite.deleted_at.is_(None),
		)
	)
	if site is None:
		raise NotFoundException("Công trình không tồn tại")

	if site.owner_id != current_user.id:
		raise ForbiddenException("Chỉ chủ công trình mới có quyền xóa thành viên")

	if db.get(User, user_id) is None:
		raise NotFoundException("Người dùng không tồn tại")

	member = db.scalar(
		select(SiteMember).where(
			SiteMember.site_id == site_id,
			SiteMember.user_id == user_id,
		)
	)
	if member is None:
		raise NotFoundException("Thành viên không thuộc công trình")

	if member.role == "OWNER":
		owner_count = db.scalar(
			select(func.count())
			.select_from(SiteMember)
			.where(
				SiteMember.site_id == site_id,
				SiteMember.role == "OWNER",
			)
		)
		if owner_count <= 1:
			raise ConflictException("Không thể xóa owner cuối cùng của công trình")

	db.delete(member)
	db.commit()
	log_audit_event(
		"REMOVE_MEMBER",
		actor_id=current_user.id,
		site_id=site_id,
		target_user_id=user_id,
	)
