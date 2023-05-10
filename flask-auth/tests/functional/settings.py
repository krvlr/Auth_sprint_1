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
        env_file = ".env.tests"


class RedisSettings(BaseSettings):
    host: str = Field(default="127.0.0.1", env="AUTH_REDIS_HOST")
    port: str = Field(default="6379", env="AUTH_REDIS_PORT")

    class Config:
        env_file = ".env.tests"


class AuthApiSettings(BaseSettings):
    host: str = Field(default="127.0.0.1", env="AUTH_API_HOST")
    port: str = Field(default="8000", env="AUTH_API_PORT")
    uri: str = Field(default="/api/v1", env="AUTH_API_URI")
    protocol: str = Field(default="http", env="AUTH_API_PROTOCOL")

    def get_api_uri(self) -> str:
        return f"{self.protocol}://{self.host}:{self.port}/{self.uri}"

    class Config:
        env_file = ".env.tests"


redis_settings = RedisSettings()
auth_api_settings = AuthApiSettings()
