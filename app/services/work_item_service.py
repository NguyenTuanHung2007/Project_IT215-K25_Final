from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException
from app.models.site import ConstructionSite, SiteMember
from app.models.user import User
from app.models.work_item import WorkItem


def get_work_item_for_user(db: Session,work_item_id: int,current_user: User,) -> WorkItem:
	member_of_site = select(SiteMember.site_id).where(
		SiteMember.site_id == WorkItem.site_id,
		SiteMember.user_id == current_user.id,
	).exists()

	query = (
		select(WorkItem)
		.join(ConstructionSite, ConstructionSite.id == WorkItem.site_id)
		.where(
			WorkItem.id == work_item_id,
			ConstructionSite.deleted_at.is_(None),
			or_(ConstructionSite.owner_id == current_user.id, member_of_site),
		)
	)
	work_item = db.scalar(query)
	if work_item is None:
		raise NotFoundException("Công việc không tồn tại hoặc bạn không thuộc công trình")

	return work_item


def update_work_item_for_user(db: Session, work_item_id: int,current_user: User,data: dict,) -> WorkItem:
	work_item = get_work_item_for_user(db, work_item_id, current_user)

	if "site_id" in data and data["site_id"] != work_item.site_id:
		target_site_access = (
			select(ConstructionSite.id)
			.outerjoin(SiteMember, SiteMember.site_id == ConstructionSite.id)
			.where(
				ConstructionSite.id == data["site_id"],
				ConstructionSite.deleted_at.is_(None),
				or_(
					ConstructionSite.owner_id == current_user.id,
					SiteMember.user_id == current_user.id,
				),
			)
		)
		if db.scalar(target_site_access) is None:
			raise NotFoundException("Công trình đích không tồn tại hoặc bạn không thuộc công trình")

	for field, value in data.items():
		setattr(work_item, field, value)

	db.commit()
	db.refresh(work_item)
	return work_item