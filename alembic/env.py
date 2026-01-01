from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv
import os

from app.database import Base
from app.models.user import User  # import ALL models

# Load .env
load_dotenv()

config = context.config
fileConfig(config.config_file_name)

# Use sync DB URL for Alembic
DATABASE_URL = os.getenv("DATABASE_URL").replace(
    "postgresql+asyncpg", "postgresql"
)

config.set_main_option("sqlalchemy.url", DATABASE_URL)

target_metadata = Base.metadata


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
