from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url:str="sqlite+aiosqlite:///chat.db"
    admin_username:str="admin"
    admin_password:str="admin123"
settings=Settings()
