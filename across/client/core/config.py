from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    """
    Base configuratiaon for across.client
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class Config(BaseConfig):
    """
    Core configuratiaon for across.client
    """

    HOST: str = "https://server.dev.across.smce.nasa.gov/api/v1"
    ACROSS_SERVER_ID: str | None = None
    ACROSS_SERVER_SECRET: str | None = None


config = Config()
