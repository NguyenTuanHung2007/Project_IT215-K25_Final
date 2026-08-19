from fastapi import FastAPI

from core.handlers import register_exception_handlers
from db import Base, engine
from models import *
from routers import app_router


app = FastAPI(title="Construction Management API")

Base.metadata.create_all(bind=engine)

register_exception_handlers(app)
app.include_router(app_router)
