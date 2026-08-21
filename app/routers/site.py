from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.auth_schema import ConstructionSiteCreate, ConstructionSiteResponse
from app.services.site_service import create_site, list_sites


sites_router = APIRouter(prefix="/construction-sites", tags=["Construction Sites"])

@sites_router.post("", response_model=ConstructionSiteResponse, status_code=status.HTTP_201_CREATED)
def post_site(site_data: ConstructionSiteCreate,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
	return create_site(
		db,
		current_user=current_user,
		name=site_data.name,
		description=site_data.description,
	)


@sites_router.get("", response_model=list[ConstructionSiteResponse])
def get_sites(search: str | None = Query(default=None), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
	return list_sites(db, current_user=current_user, search=search)
