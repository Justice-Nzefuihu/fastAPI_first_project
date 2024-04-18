# database_hostname : str
# database_port : intfrom pydantic import BaseSettings
# databasefrom pydant_password : stric import BaseSettings
# databasefrom pydantic import BaseS_name : strettings
# databasefrom pydantic import BaseSettings_username : str
# secret_key : str
# algorithm : str
# access_token_expires_minutes : int
from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    database_hostname : str
    database_port : int
    database_password : str
    database_name : str
    database_username : str
    secret_key : str
    algorithm : str
    access_token_expire_minutes : int

    class Config:
        env_file = ".env"


setting = Setting()

