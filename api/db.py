from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, TIMESTAMP, text
import datetime
from api.config import settings

engine=create_async_engine(settings.database_url, echo=False)
AsyncSessionLocal=async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase): pass

class User(Base):
    __tablename__="user"
    id:Mapped[int]=mapped_column(Integer, primary_key=True, autoincrement=True)
    username:Mapped[str]=mapped_column(String, unique=True)
    password:Mapped[str]=mapped_column(String)
    role:Mapped[str]=mapped_column(String, default="normal")

class MoodLog(Base):
    __tablename__="mood_log"
    id:Mapped[int]=mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id:Mapped[str]=mapped_column(String)
    emotion:Mapped[str]
    score:Mapped[float]
    ts:Mapped[datetime.datetime]=mapped_column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
