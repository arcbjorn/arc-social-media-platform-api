from pydantic import BaseSettings


class Settings(BaseSettings):
    db_hostname: str
    db_port: str
    db_password: str
    db_name: str
    db_username: str = "postgres"

    secret_key: str = "23wetrhdfjnw4543"
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


env = Settings()
