import sys
from pathlib import Path

if __package__ in (None, ""):
	sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
 
from fastapi import FastAPI
from app.core.handlers import register_exception_handlers
from app.db import Base, engine
from app.models import *
from app.routers import app_router
from app.routers.auth import router as auth_router
from app.routers.site import sites_router
from app.routers.users import users_router


app = FastAPI(title="Construction Management API")

Base.metadata.create_all(bind=engine)

register_exception_handlers(app)
app.include_router(app_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(sites_router)
