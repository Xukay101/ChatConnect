from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = 'ChatConnect'
    APP_PREFIX: str = '/api'

    # Getting .env variables
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    DATABASE_URI: str

settings = Settings()
