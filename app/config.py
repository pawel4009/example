from pydantic import BaseSettings

# environment variables: pydantic will look for them case insensitive and validate them
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # we define our variables in the .env file, that is never going to be pushed to the repo
    class Config:
        env_file = ".env"

settings = Settings()
