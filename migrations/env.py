import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from config import get_settings
from db.db_setup import Base

# Alembic Config object
config = context.config
fileConfig(config.config_file_name)

# Load database URL from settings
settings = get_settings()
DATABASE_URL = settings.DATABASE_URL

# Target metadata for migrations
target_metadata = Base.metadata


def do_run_migrations(connection):
    """
    Runs migrations using the connection.
    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """
    Run migrations in 'online' mode for AsyncEngine.
    """
    connectable = create_async_engine(DATABASE_URL, future=True)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


# Run migrations
asyncio.run(run_migrations_online())
