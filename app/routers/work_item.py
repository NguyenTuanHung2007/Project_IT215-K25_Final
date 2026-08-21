from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.auth_schema import WorkItemResponse, WorkItemUpdate
from app.services.work_item_service import (
	get_work_item_for_user,
	update_work_item_for_user,
)

work_items_router = APIRouter(prefix="/work-items", tags=["Work Items"])

@work_items_router.get("/{work_item_id}", response_model=WorkItemResponse)
def get_work_item(work_item_id: int,current_user: User = Depends(get_current_user),db: Session = Depends(get_db),):
	return get_work_item_for_user(db, work_item_id, current_user)


@work_items_router.patch("/{work_item_id}",response_model=WorkItemResponse,status_code=status.HTTP_200_OK,)
def update_work_item(work_item_id: int,data: WorkItemUpdate,current_user: User = Depends(get_current_user),db: Session = Depends(get_db),):
	return update_work_item_for_user(
		db,
		work_item_id,
		current_user,
		data.model_dump(exclude_unset=True),
	)
