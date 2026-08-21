from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
	db_user: str
	db_password: str
	db_host: str
	db_port: int
	db_name: str
	secret_key: str
	jwt_algorithm: str = "HS256"
	access_token_expire_minutes: int = 30
	refresh_token_expire_minutes: int = 10080

	model_config = SettingsConfigDict(
		env_file=BASE_DIR / ".env",
		env_file_encoding="utf-8",
		extra="ignore",
	)


settings = Settings()
