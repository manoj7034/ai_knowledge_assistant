import app.models  # noqa: F401

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.config.settings import settings
from app.database.base import Base

# Alembic Config object
config = context.config

# Use the database URL from application settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Configure Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# SQLAlchemy metadata used for autogeneration
target_metadata = Base.metadata


def include_object(object, name, type_, reflected, compare_to):
    """
    Include only objects that belong to our application schema.

    This prevents Alembic from detecting tables belonging to
    other projects/databases that exist in the same PostgreSQL
    instance.
    """
    if type_ == "table":
        return object.schema == settings.DB_SCHEMA

    return True


def get_alembic_context_kwargs():
    """
    Common Alembic configuration shared by both
    offline and online migrations.
    """
    return {
        "target_metadata": target_metadata,
        "include_schemas": True,
        "include_object": include_object,
        "version_table_schema": settings.DB_SCHEMA,
        "compare_type": True,
        "compare_server_default": True,
    }


def run_migrations_offline() -> None:
    """
    Run migrations in offline mode.
    """

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        **get_alembic_context_kwargs(),
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in online mode.
    """

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            **get_alembic_context_kwargs(),
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()