from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
	db_user: str
	db_password: str
	db_host: str
	db_port: int
	db_name: str

	model_config = SettingsConfigDict(
		env_file=BASE_DIR / ".env",
		env_file_encoding="utf-8",
		extra="ignore",
	)


settings = Settings()
