from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.site import ConstructionSite


def list_sites(db: Session, search: str | None = None) -> list[ConstructionSite]:
	query = select(ConstructionSite).order_by(ConstructionSite.id)

	if search:
		query = query.where(ConstructionSite.name.ilike(f"%{search.strip()}%"))

	return list(db.scalars(query).all())
