from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession


# TODO  Vector Database Repository
class BaseVectorRepository:
    def __init__(self, async_session: SQLAlchemyAsyncSession):
        self.async_session = async_session
