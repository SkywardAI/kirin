import typing
from typing import Optional

import sqlalchemy

from src.models.db.chat import ChatHistory, Session
from src.models.schemas.chat import SessionUpdate
from src.repository.crud.base import BaseCRUDRepository
from src.utilities.exceptions.database import EntityDoesNotExist


class SessionCRUDRepository(BaseCRUDRepository):
    async def create_session(self, account_id: Optional[int], name: str) -> Session:
        new_session = Session(account_id=account_id, name=name)

        self.async_session.add(instance=new_session)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_session)

        return new_session

    async def read_sessions(self) -> typing.Sequence[Session]:
        stmt = sqlalchemy.select(Session).order_by(Session.created_at.desc())
        query = await self.async_session.execute(statement=stmt)
        return query.scalars().all()

    async def read_sessions_by_uuid(self, session_uuid: str) -> Session:
        stmt = sqlalchemy.select(Session).where(Session.uuid == session_uuid).order_by(Session.created_at.desc())
        query = await self.async_session.execute(statement=stmt)
        session = query.scalar()
        if session is None:
            raise EntityDoesNotExist("Session with uuid `{session_uuid}` does not exist!")

        return session  # type: ignore

    async def update_sessions_by_uuid(self, session: SessionUpdate, account_id: int) -> Session:
        stmt = sqlalchemy.select(Session).where(Session.uuid == session.sessionUuid, Session.account_id == account_id)
        query = await self.async_session.execute(statement=stmt)
        update_session = query.scalar()
        if update_session is None:
            raise EntityDoesNotExist(f"Session with uuid `{session.sessionUuid}` does not exist!")
        update_stmt = sqlalchemy.update(table=Session).where(Session.uuid == session.sessionUuid).values(updated_at=sqlalchemy_functions.now())  # type: ignore
        if session["name"]:
            update_stmt = update_stmt.values(username=session["name"])

        if session["type"]:
            update_stmt = update_stmt.values(type=session["type"])
        await self.async_session.execute(statement=update_stmt)
        await self.async_session.commit()
        await self.async_session.refresh(instance=update_session)

        return update_session  # type: ignore

    async def read_create_sessions_by_uuid(self, session_uuid: str, account_id: int, name: str) -> Session:
        stmt = sqlalchemy.select(Session).where(Session.uuid == session_uuid)
        query = await self.async_session.execute(statement=stmt)
        session = query.scalar()
        if session is None:
            new_session = Session(account_id=account_id, name=name)

            self.async_session.add(instance=new_session)
            await self.async_session.commit()
            await self.async_session.refresh(instance=new_session)
            return new_session
        else:
            return session  # type: ignore

    async def read_sessions_by_account_id(self, id: int) -> typing.Sequence[Session]:
        # stmt = sqlalchemy.select(Session).where(Session.account_id == id)
        stmt = sqlalchemy.select(Session).where(Session.account_id == id)
        query = await self.async_session.execute(statement=stmt)
        return query.scalars().all()

    async def verify_session_by_account_id(self, session_uuid: str, account_id: int ) -> bool:
        # stmt = sqlalchemy.select(Session).where(Session.account_id == id)
        stmt = sqlalchemy.select(Session).where(Session.uuid == session_uuid, Session.account_id == account_id)
        query = await self.async_session.execute(statement=stmt)
        return bool(query)

class ChatHistoryCRUDRepository(BaseCRUDRepository):
    async def read_chat_history_by_id(self, id: int) -> ChatHistory:
        stmt = sqlalchemy.select(ChatHistory).where(ChatHistory.id == id)
        query = await self.async_session.execute(statement=stmt)
        chat_history =query.scalar()
        if chat_history is None:
            raise EntityDoesNotExist("ChatHistory with id `{id}` does not exist!")

        return chat_history # type: ignore

    async def read_chat_history_by_session_id(self, id: int, limit_num=50) -> typing.Sequence[ChatHistory]:
        # TODO limit num = 50 is a temp number
        stmt = (
            sqlalchemy.select(ChatHistory)
            .where(ChatHistory.session_id == id)
            .order_by(ChatHistory.created_at.desc())
            .limit(limit_num)
        )
        query = await self.async_session.execute(statement=stmt)
        return query.scalars().all()  # type: ignore
