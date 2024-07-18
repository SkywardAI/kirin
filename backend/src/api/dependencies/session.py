import typing
import loguru
from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession

from src.repository.database import async_db

#TODO async session need to support background task
async def get_async_session() -> typing.AsyncGenerator[SQLAlchemyAsyncSession, None]:
    try:
        yield async_db.async_session
    except Exception as e:
        loguru.logger.info(f"Exception --- {e}")
        await async_db.async_session.rollback()
        raise
    finally:
        await async_db.async_session.close()
