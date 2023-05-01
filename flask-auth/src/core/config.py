import logging

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_host: str = Field(default="127.0.0.1", env="DB_HOST")
    db_port: str = Field(default=5432, env="DB_PORT")
    db_name: str = Field(default="auth_db", env="DB_NAME")
    db_user: str = Field(default="", env="DB_USER")
    db_password: str = Field(default="", env="DB_PASSWORD")

    def get_db_url(self) -> str:
        return (
            f"postgresql://{self.db_user}:{self.db_password}@"
            f"{self.db_host}:{self.db_port}/{self.db_name}"
        )

    redis_host: str = Field(default="127.0.0.1", env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")

    debug_log_level: bool = Field(default=False, env="DEBUG")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", env="LOG_FORMAT"
    )
    log_default_handlers = ["console"]

    class Config:
        env_file = ".env"


settings = Settings()

log_level = logging.DEBUG if settings.debug_log_level else logging.INFO
