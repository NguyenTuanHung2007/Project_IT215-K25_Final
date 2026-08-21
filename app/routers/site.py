from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.auth_schema import (
	ConstructionSiteCreate,
	ConstructionSiteResponse,
	ConstructionSiteUpdate,
	SiteMemberResponse,
)
from app.services.site_service import (
	add_site_member,
	create_site,
	delete_site,
	list_sites,
	remove_site_member,
	update_site,
)


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


@sites_router.put("/{site_id}", response_model=ConstructionSiteResponse)
def put_site(
	site_id: int,
	site_data: ConstructionSiteUpdate,
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db),
):
	return update_site(
		db,
		site_id,
		current_user,
		site_data.model_dump(exclude_unset=True),
	)


@sites_router.patch("/{site_id}", response_model=ConstructionSiteResponse)
def patch_site(site_id: int,site_data: ConstructionSiteUpdate,current_user: User = Depends(get_current_user),db: Session = Depends(get_db),):
	return update_site(
		db,
		site_id,
		current_user,
		site_data.model_dump(exclude_unset=True),
	)


@sites_router.delete("/{site_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_site_endpoint(site_id: int,current_user: User = Depends(get_current_user),db: Session = Depends(get_db),) -> None:
	delete_site(db, site_id, current_user)


@sites_router.post("/{site_id}/members/{user_id}", response_model=SiteMemberResponse, status_code=status.HTTP_201_CREATED)
def post_site_member(site_id: int,user_id: int,current_user: User = Depends(get_current_user),db: Session = Depends(get_db),):
	return add_site_member(db, site_id, user_id, current_user)


@sites_router.delete("/{site_id}/members/{user_id}",status_code=status.HTTP_204_NO_CONTENT,)
def delete_site_member(site_id: int,user_id: int,current_user: User = Depends(get_current_user),db: Session = Depends(get_db),) -> None:
	remove_site_member(db, site_id, user_id, current_user)
