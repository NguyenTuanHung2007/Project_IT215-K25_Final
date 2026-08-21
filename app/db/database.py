from urllib.parse import quote_plus

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

DATABASE_URL = (
    f"mysql+pymysql://{quote_plus(settings.db_user)}:{quote_plus(settings.db_password)}"
    f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()


def ensure_schema() -> None:
    columns = {column["name"] for column in inspect(engine).get_columns("construction_sites")}
    if "deleted_at" not in columns:
        with engine.begin() as connection:
            connection.execute(
                text("ALTER TABLE construction_sites ADD COLUMN deleted_at DATETIME NULL")
            )
