import sys
from pathlib import Path

if __package__ in (None, ""):
	sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
 
from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.handlers import register_exception_handlers
from app.db import Base, engine
from app.models import *
from app.routers import app_router
from app.routers.auth import limiter as auth_limiter
from app.routers.auth import router as auth_router
from app.routers.site import sites_router
from app.routers.users import users_router
from app.routers.work_item import work_items_router


app = FastAPI(title="Construction Management API")
app.state.limiter = auth_limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

Base.metadata.create_all(bind=engine)

register_exception_handlers(app)
app.include_router(app_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(sites_router)
app.include_router(work_items_router)
