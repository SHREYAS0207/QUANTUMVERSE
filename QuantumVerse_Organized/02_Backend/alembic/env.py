import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy import pool
from alembic import context

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from app.models.user        import Base as UserBase
from app.models.circuit     import Base as CircuitBase
from app.models.learning    import Base as LearningBase
from app.models.quiz        import Base as QuizBase
from app.models.ai          import Base as AIBase

target_metadata = [UserBase.metadata, CircuitBase.metadata, LearningBase.metadata,
                   QuizBase.metadata, AIBase.metadata]


def run_migrations_offline():
    context.configure(url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"})
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    cfg = config.get_section(config.config_ini_section)
    connectable = async_engine_from_config(cfg, prefix="sqlalchemy.", poolclass=pool.NullPool)
    async with connectable.connect() as connection:
        await connection.run_sync(lambda conn: context.configure(connection=conn, target_metadata=target_metadata))
        async with connection.begin():
            await connection.run_sync(lambda _: context.run_migrations())
    await connectable.dispose()


def run_migrations_online():
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
