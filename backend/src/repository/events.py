import fastapi
import loguru
from sqlalchemy import event
from sqlalchemy.dialects.postgresql.asyncpg import AsyncAdapt_asyncpg_connection
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.pool.base import _ConnectionRecord

from src.config.settings.const import ANONYMOUS_USER, ANONYMOUS_EMAIL, ANONYMOUS_PASS
from src.config.manager import settings
from src.models.db.account import Account
from src.securities.hashing.password import pwd_generator
from src.repository.database import async_db
from src.repository.table import Base
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

async def initialize_anonymous_user(async_session: AsyncSession) -> None:
    loguru.logger.info("Anonymous user --- Creating . . .")

    new_account = Account(username=ANONYMOUS_USER, email=ANONYMOUS_EMAIL, is_logged_in=True)

    new_account.set_hash_salt(hash_salt=pwd_generator.generate_salt)
    new_account.set_hashed_password(
        hashed_password=pwd_generator.generate_hashed_password(
        hash_salt=new_account.hash_salt, new_password=ANONYMOUS_PASS
        )
    )

    async_session.add(instance=new_account)
    await async_session.commit()
    await async_session.refresh(instance=new_account)

    loguru.logger.info("Anonymous user --- Successfully Created!")

async def initialize_admin_user(async_session: AsyncSession) -> None:
    loguru.logger.info("Admin user --- Creating . . .")

    new_account = Account(username=settings.ADMIN_USERNAME, email=settings.ADMIN_EMAIL, is_logged_in=True)

    new_account.set_hash_salt(hash_salt=pwd_generator.generate_salt)
    new_account.set_hashed_password(
        hashed_password=pwd_generator.generate_hashed_password(
        hash_salt=new_account.hash_salt, new_password=settings.ADMIN_USERNAME
        )
    )

    async_session.add(instance=new_account)
    await async_session.commit()
    await async_session.refresh(instance=new_account)

    loguru.logger.info("Admin user --- Successfully Created!")

async def initialize_db_connection(backend_app: fastapi.FastAPI) -> None:
    loguru.logger.info("Database Connection --- Establishing . . .")

    backend_app.state.db = async_db

    async with backend_app.state.db.async_engine.begin() as connection:
        await initialize_db_tables(connection=connection)
    async with async_db.async_session as async_session:
        await initialize_anonymous_user(async_session=async_session)
        await initialize_admin_user(async_session=async_session)

    loguru.logger.info("Database Connection --- Successfully Established!")


async def initialize_vectordb_collection() -> None:
    
    loguru.logger.info("Vector Database Connection --- Establishing . . .")
    # RAG data can be loaded manually from the frontend
    # https://github.com/SkywardAI/chat-backend/issues/172
    vector_db.create_collection()
    # Create sample embeddings for testing
    # Sample can be loaded either dataset or directly from strings
    # For network consideration, default method is to use strings
    # Dataset examples are shown as following
    # embedding_list=load_dataset('aisuko/sentences_of_Melbourne')
    # ps=embedding_list['train'].to_pandas().to_numpy()
    # vector_db.insert_list(ps, SAMPLE_CONTEXT)
    # embedding_list = ai_model.encode_string(SAMPLE_CONTEXT)
    # vector_db.insert_list(embedding_list, SAMPLE_CONTEXT)
    loguru.logger.info("Vector Database Connection --- Successfully Established!")


async def dispose_db_connection(backend_app: fastapi.FastAPI) -> None:
    loguru.logger.info("Database Connection --- Disposing . . .")

    await backend_app.state.db.async_engine.dispose()

    loguru.logger.info("Database Connection --- Successfully Disposed!")
