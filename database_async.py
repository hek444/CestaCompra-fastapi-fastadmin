import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator

# Carga entorno
dotenv_path = load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Engine asíncrono y sesión
engine = create_async_engine(DATABASE_URL, echo=True)
async_sessionmaker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_sessionmaker() as session:
        yield session