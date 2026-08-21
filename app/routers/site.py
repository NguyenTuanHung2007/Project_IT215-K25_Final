from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.auth_schema import (
	ConstructionSiteCreate,
	ConstructionSiteResponse,
	ConstructionSiteUpdate,
	SiteMemberAdd,
	SiteMemberResponse,
)
from app.services.site_service import (
	add_site_member,
	create_site,
	delete_site,
	get_site_for_user,
	list_sites,
	list_site_members,
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


@sites_router.get("/{site_id}", response_model=ConstructionSiteResponse)
def get_site(site_id: int,current_user: User = Depends(get_current_user),db: Session = Depends(get_db),):
	return get_site_for_user(db, site_id, current_user)


@sites_router.get("/{site_id}/members", response_model=list[SiteMemberResponse])
def get_site_members(site_id: int,current_user: User = Depends(get_current_user),db: Session = Depends(get_db),):
	return list_site_members(db, site_id, current_user)


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


@sites_router.post("/{site_id}/members", response_model=SiteMemberResponse, status_code=status.HTTP_201_CREATED)
def post_site_member(site_id: int,data: SiteMemberAdd,current_user: User = Depends(get_current_user),db: Session = Depends(get_db),):
	return add_site_member(db, site_id, data.user_id, current_user)


@sites_router.delete("/{site_id}/members/{user_id}",status_code=status.HTTP_204_NO_CONTENT,)
def delete_site_member(site_id: int,user_id: int,current_user: User = Depends(get_current_user),db: Session = Depends(get_db),) -> None:
	remove_site_member(db, site_id, user_id, current_user)
