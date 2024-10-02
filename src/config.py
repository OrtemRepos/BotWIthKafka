from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    token: str
    bootstrap_server: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Config()  # type: ignore
