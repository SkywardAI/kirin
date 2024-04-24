import fastapi
import loguru
from sqlalchemy import event
from sqlalchemy.dialects.postgresql.asyncpg import AsyncAdapt_asyncpg_connection
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSessionTransaction
from sqlalchemy.pool.base import _ConnectionRecord

from src.config.settings.const import SAMPLE_CONTEXT
from src.repository.database import async_db
from src.repository.table import Base
from src.repository.vector_database import vector_db
from src.repository.ai_models import ai_model
from datasets import load_dataset
from src.repository.vector_database import vector_db

@event.listens_for(target=async_db.async_engine.sync_engine, identifier="connect")
def inspect_db_server_on_connection(
    db_api_connection: AsyncAdapt_asyncpg_connection, connection_record: _ConnectionRecord
) -> None:
    loguru.logger.info(f"New DB API Connection ---\n {db_api_connection}")
    loguru.logger.info(f"Connection Record ---\n {connection_record}")


@event.listens_for(target=async_db.async_engine.sync_engine, identifier="close")
def inspect_db_server_on_close(
    db_api_connection: AsyncAdapt_asyncpg_connection, connection_record: _ConnectionRecord
) -> None:
    loguru.logger.info(f"Closing DB API Connection ---\n {db_api_connection}")
    loguru.logger.info(f"Closed Connection Record ---\n {connection_record}")


async def initialize_db_tables(connection: AsyncConnection) -> None:
    loguru.logger.info("Database Table Creation --- Initializing . . .")

    await connection.run_sync(Base.metadata.drop_all)
    await connection.run_sync(Base.metadata.create_all)

    loguru.logger.info("Database Table Creation --- Successfully Initialized!")


async def initialize_db_connection(backend_app: fastapi.FastAPI) -> None:
    loguru.logger.info("Database Connection --- Establishing . . .")

    backend_app.state.db = async_db

    async with backend_app.state.db.async_engine.begin() as connection:
        await initialize_db_tables(connection=connection)

    loguru.logger.info("Database Connection --- Successfully Established!")

async def initialize_aimodel() -> None:
    loguru.logger.info("Ai model --- Initializing . . .")
    await ai_model.init()

    loguru.logger.info("Ai model--- Successfully Initialized!")

async def initialize_vectordb_connection() -> None:
    loguru.logger.info("Vector Database Connection --- Establishing . . .")

    vector_db.create_collection()
    # Create sample embeddings for testing
    # embedding_list=load_dataset('aisuko/sentences_of_Melbourne')
    # ps=embedding_list['train'].to_pandas().to_numpy()
    # vector_db.insert_list(ps, SAMPLE_CONTEXT)
    embedding_list = ai_model.encode_string(SAMPLE_CONTEXT)
    vector_db.insert_list(embedding_list, SAMPLE_CONTEXT)
    print("Sample inserted")
    loguru.logger.info("Vector Database Connection --- Successfully Established!")


async def dispose_db_connection(backend_app: fastapi.FastAPI) -> None:
    loguru.logger.info("Database Connection --- Disposing . . .")

    await backend_app.state.db.async_engine.dispose()

    loguru.logger.info("Database Connection --- Successfully Disposed!")
