from fastapi import FastAPI

from app.core.handlers import register_exception_handlers
from app.db import Base, engine
from app.models import *
from app.routers import app_router


app = FastAPI(title="Construction Management API")

Base.metadata.create_all(bind=engine)

register_exception_handlers(app)
app.include_router(app_router)
