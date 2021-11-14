from pydantic import BaseSettings


class Settings(BaseSettings):
    db_hostname: str = "localhost"
    db_port: str = "5432"
    db_password: str = "password"
    db_name: str = "postgres"
    db_username: str = "postgres"

    secret_key: str = "23wetrhdfjnw4543"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


env = Settings()
