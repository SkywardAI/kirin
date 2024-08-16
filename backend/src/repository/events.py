# coding=utf-8

# Copyright [2024] [SkywardAI]
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import fastapi
import lancedb
import loguru

from datetime import datetime
from src.models.meta import Account as newAccount

from sqlalchemy import event
from sqlalchemy.dialects.postgresql.asyncpg import AsyncAdapt_asyncpg_connection
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.pool.base import _ConnectionRecord

from src.config.settings.const import ANONYMOUS_USER, ANONYMOUS_EMAIL, ANONYMOUS_PASS, META_LANCEDB
from src.config.manager import settings
from src.models.db.account import Account
from src.securities.hashing.password import pwd_generator
from src.repository.database import async_db
from src.repository.table import Base
from src.utilities.httpkit.httpx_kit import httpx_kit


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

async def initialize_meta_table( db: lancedb.db) -> None:
    loguru.logger.info("Meta Table Creation --- Initializing . . .")
    tbl = db.create_table("account", schema = newAccount, mode="overwrite")
    await initialize_meta_data( tbl )
    loguru.logger.info("Meta Table Creation --- Successfully Initialized!")
    
async def initialize_meta_data( tbl: lancedb.table.Table) -> None:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tbl.add([{
        "username": ANONYMOUS_USER,
        "email": ANONYMOUS_EMAIL,
        "_hashed_password": pwd_generator.generate_hashed_password(
            hash_salt=pwd_generator.generate_salt, new_password=ANONYMOUS_PASS
        ),
        "_hash_salt": pwd_generator.generate_salt,
        "is_active": True,
        "created_at": current_time,
        "updated_at": current_time
    }])
    loguru.logger.info("Anonymous user added!")
    tbl.add([{
        "username": settings.ADMIN_USERNAME,
        "email": settings.ADMIN_EMAIL,
        "_hashed_password": pwd_generator.generate_hashed_password(
            hash_salt=pwd_generator.generate_salt, new_password=settings.ADMIN_PASS
        ),
        "_hash_salt": pwd_generator.generate_salt,
        "is_active": True,
        "created_at": current_time,
        "updated_at": current_time
    }])
    loguru.logger.info("Admin user added!")

async def initialize_default_data() -> None:
    async with async_db.async_session_maker() as async_session:
        await initialize_anonymous_user(async_session=async_session)
        await initialize_admin_user(async_session=async_session)

async def initialize_meta_database() -> None:
    loguru.logger.info("Meta database initializing . . .")
    meta_db = lancedb.connect(META_LANCEDB)
    await initialize_meta_table( meta_db )
    loguru.logger.info("Meta database initialized!")

async def initialize_db_connection(backend_app: fastapi.FastAPI) -> None:
    loguru.logger.info("Database Connection --- Establishing . . .")

    backend_app.state.db = async_db

    async with backend_app.state.db.async_engine.begin() as connection:
        await initialize_db_tables(connection=connection)

    loguru.logger.info("Database Connection --- Successfully Established!")


async def dispose_db_connection(backend_app: fastapi.FastAPI) -> None:
    loguru.logger.info("Database Connection --- Disposing . . .")

    await backend_app.state.db.async_engine.dispose()

    loguru.logger.info("Database Connection --- Successfully Disposed!")


async def dispose_httpx_client() -> None:
    loguru.logger.info("Httpx Client --- Disposing . . .")

    close_async = await httpx_kit.teardown_async_client()

    loguru.logger.info(
        "Httpx Async Client --- Successfully Disposed!" if close_async else "Httpx Async Client --- Failed to Dispose!"
    )

    close_sync = httpx_kit.teardown_sync_client()

    loguru.logger.info(
        "Httpx Sync Client --- Successfully Disposed!" if close_sync else "Httpx Sync Client --- Failed to Dispose!"
    )
