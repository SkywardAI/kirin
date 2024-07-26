import typing
import loguru
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.database import async_db


async def get_async_session() -> typing.AsyncGenerator[AsyncSession, None]:
    try:
        async with async_db.async_session_maker() as async_session:
            yield async_session
        loguru.logger.info(f"Async pool:{async_db.pool.status()}")
    except Exception as e:
        loguru.logger.info(f"Exception --- {e}")
        await async_session.rollback()
        raise
    else:
        # https://github.com/grillazz/fastapi-sqlalchemy-asyncpg/issues/63
        await async_session.commit()
    finally:
        await async_session.close()
