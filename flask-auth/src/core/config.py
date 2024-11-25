from pathlib import Path

from pydantic import BaseSettings, Field

BASE_DIR = Path(__file__).resolve().parent.parent
MIGRATION_DIR = BASE_DIR / "db" / "migrations"


class LoggerSettings(BaseSettings):
    level: str = Field(default="INFO", env="LOGGING_LEVEL")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", env="LOG_FORMAT"
    )
    default_handlers: list = ["console"]


class FlaskSettings(BaseSettings):
    debug: bool = Field(default=True)
    host: str = Field(default="0.0.0.0")
    port: str = Field(default="8000")

    class Config:
        env_file = ".env"


class PostgreSettings(BaseSettings):
    host: str = Field(default="127.0.0.1", env="AUTH_DB_HOST")
    port: str = Field(default="5432", env="AUTH_DB_PORT")
    name: str = Field(default="auth_database", env="AUTH_DB_NAME")
    user: str = Field(default="admin", env="AUTH_DB_USER")
    password: str = Field(default="admin", env="AUTH_DB_PASSWORD")

    def get_db_uri(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    class Config:
        env_file = ".env"


class RedisSettings(BaseSettings):
    host: str = Field(default="127.0.0.1", env="AUTH_REDIS_HOST")
    port: str = Field(default="6379", env="AUTH_REDIS_PORT")

    class Config:
        env_file = ".env"


class JWTSettings(BaseSettings):
    cookie_secure: str = Field(default="False", repr=False, env="JWT_COOKIE_SECURE")
    token_location: str = Field(default="cookies", repr=False, env="JWT_TOKEN_LOCATION")
    secret_key: str = Field(default="SUPER-SECRET-KEY", repr=False, env="JWT_SECRET_KEY")
    access_token_expires: int = Field(default=1, env="JWT_ACCESS_TOKEN_EXPIRES")
    refresh_token_expires: int = Field(default=30, env="JWT_REFRESH_TOKEN_EXPIRES")

    class Config:
        env_file = ".env"


class RoleSettings(BaseSettings):
    default_user_role: str = Field(default="default", env="DEFAULT_USER_ROLE")
    initial_user_roles: str = Field(default="default", env="INITIAL_USER_ROLES")
    initial_user_descrition_roles: str = Field(
        default="Base rights for a registered user", env="INITIAL_USER_DESCRIPTION_ROLES"
    )

    def get_initial_roles(self):
        for role, descrition in zip(
            self.initial_user_roles.split(", "), self.initial_user_descrition_roles.split(", ")
        ):
            yield role, descrition

    class Config:
        env_file = ".env"


logger_settings = LoggerSettings()
flask_settings = FlaskSettings()
postgre_settings = PostgreSettings()
redis_settings = RedisSettings()
jwt_settings = JWTSettings()
role_settings = RoleSettings()
