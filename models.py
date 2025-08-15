from dotenv import load_dotenv
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker,AsyncAttrs
from sqlalchemy.orm import DeclarativeBase,MappedColumn,Mapped
from sqlalchemy import Integer, String, JSON

load_dotenv()

POSTGRES_USER=os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB=os.getenv("POSTGRES_DB","asincio_db_1")
POSTGRES_HOST=os.getenv("POSTGRES_HOST","localhost")
POSTGRES_PORT=os.getenv("POSTGRES_PORT",5432)


DSN = (f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
       f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")

engine = create_async_engine(DSN)

Session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase,AsyncAttrs):
    pass

class SwapiPeople(Base):
    __tablename__ = "swapi_people"
    id: Mapped[int] = MappedColumn(Integer, primary_key=True)
    json: Mapped[dict] = MappedColumn(JSON)

async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_orm():
    await  engine.dispose()
