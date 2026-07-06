from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class BaseConfig(BaseSettings):
    """
    Base configuration for across.client
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class Config(BaseConfig):
    """
    Core configuration for across.client
    """

    ACROSS_SERVER_HOST: str = "https://api.across.sciencecloud.nasa.gov"
    ACROSS_SERVER_PORT: str = ""
    ACROSS_SERVER_ROOT_PATH: str = "/"
    ACROSS_SERVER_VERSION: str = "v1"
    ACROSS_SERVER_ID: str | None = None
    ACROSS_SERVER_SECRET: str | None = None

    @property
    def ACROSS_SERVER_URL(self) -> str:  # noqa: D102, N802 uppercase property name is intentional to match env var
        parts = [
            self.ACROSS_SERVER_HOST,
            self.ACROSS_SERVER_ROOT_PATH,
            self.ACROSS_SERVER_VERSION,
        ]

        if self.ACROSS_SERVER_PORT:
            parts.insert(1, f":{self.ACROSS_SERVER_PORT}")

        url = "".join(parts)

        # add protocol if DNE
        if not url.startswith(("http://", "https://")):
            url = f"http://{url}"

        return url


config = Config()
