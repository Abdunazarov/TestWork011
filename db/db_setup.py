from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from config import get_settings
from sqlalchemy.ext.declarative import declarative_base


settings = get_settings()

engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

async_session = sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)

Base = declarative_base()

# Async generator for database sessions
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
