from pydantic import BaseSettings, Field


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
    port: int = Field(default="6379", env="AUTH_REDIS_PORT")

    class Config:
        env_file = ".env"


postgre_settings = PostgreSettings()
redis_settings = RedisSettings()
