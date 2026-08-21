from datetime import datetime, timezone

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.site import ConstructionSite, SiteMember
from app.models.user import User


def create_site(
	db: Session,
	current_user: User,
	name: str,
	description: str | None = None,
) -> ConstructionSite:
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
	return site


def list_sites(db: Session,current_user: User,search: str | None = None,) -> list[ConstructionSite]:
	member_site = select(SiteMember.site_id).where(
		SiteMember.site_id == ConstructionSite.id,
		SiteMember.user_id == current_user.id,
	).exists()
	query = select(ConstructionSite).order_by(ConstructionSite.id)
	query = query.where(
		or_(ConstructionSite.owner_id == current_user.id, member_site)
	)

	if search:
		search_term = search.strip()
		if search_term:
			query = query.where(ConstructionSite.name.ilike(f"%{search_term}%"))

	return list(db.scalars(query).all())
