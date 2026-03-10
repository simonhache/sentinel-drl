import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    POSTGRES_USER = os.getenv("DB_USER")
    POSTGRES_PASSWORD = os.getenv("DB_PASSWORD")
    POSTGRES_DB = os.getenv("DB_NAME")
    POSTGRES_HOST = os.getenv("DB_HOST")
    POSTGRES_PORT = os.getenv("DB_PORT", "5432")

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )
