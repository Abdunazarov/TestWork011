from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from typing import AsyncGenerator
from sqlalchemy.orm import sessionmaker, declarative_base
from config import get_settings


settings = get_settings()

engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)

async_session = sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)

Base = declarative_base()

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session.begin() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
