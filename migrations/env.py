import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from db.db_setup import Base
from config import get_settings

config = context.config

fileConfig(config.config_file_name)

settings = get_settings()
DATABASE_URL = settings.DATABASE_URL

target_metadata = Base.metadata


def run_migrations_online():
    """
    Run migrations in 'online' mode for AsyncEngine.
    """
    connectable = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)

    async def do_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(context.configure, target_metadata=target_metadata)
            await connection.run_sync(context.run_migrations)

    asyncio.run(do_migrations())


# Execute online migrations
run_migrations_online()
