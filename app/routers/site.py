from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.dependencies import get_db, require_admin
from app.models.user import User
from app.schemas.auth_schema import ConstructionSiteResponse
from app.services.site_service import list_sites


sites_router = APIRouter(prefix="/sites", tags=["Construction Sites"])


@sites_router.get("", response_model=list[ConstructionSiteResponse])
def get_sites(search: str | None = Query(default=None),admin_user: User = Depends(require_admin),db: Session = Depends(get_db)):
	return list_sites(db, search=search)
