from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env", env_file_encoding="utf-8", extra="ignore"
    )

    secret_key: str = "dev-only-insecure-key-change-me"
    admin_username: str = "admin"
    admin_password: str = "admin"
    database_url: str = "sqlite:///./portfolio.db"
    cors_origins: str = "http://localhost:4321,http://127.0.0.1:4321"

    # Session cookie lifetime, seconds. 8 hours.
    session_max_age: int = 60 * 60 * 8

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def resolved_database_url(self) -> str:
        """Make a relative sqlite path resolve against backend/, not the CWD."""
        prefix = "sqlite:///./"
        if self.database_url.startswith(prefix):
            # as_posix() keeps Windows backslashes out of the URL.
            return f"sqlite:///{(BACKEND_DIR / self.database_url[len(prefix):]).as_posix()}"
        return self.database_url


settings = Settings()
