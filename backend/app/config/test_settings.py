from pydantic_settings import SettingsConfigDict

from app.config.settings import Settings


class TestSettings(Settings):
    model_config = SettingsConfigDict(
        env_file=".env.test",
        extra="ignore",
    )


test_settings = TestSettings() # type: ignore