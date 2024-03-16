import typing

import sqlalchemy
from sqlalchemy.sql import functions as sqlalchemy_functions

from src.models.db.ai_model import AiModel
from src.models.schemas.ai_model import AiModelInUpdate
from src.repository.crud.base import BaseCRUDRepository
from src.securities.verifications.credentials import credential_verifier
from src.utilities.exceptions.database import EntityAlreadyExists, EntityDoesNotExist


class AiModelCRUDRepository(BaseCRUDRepository):
    async def create_aimodel(self, aimodel_create: AiModel) -> AiModel:
        new_aimodel = AiModel(name=aimodel_create.name, des=aimodel_create.des)

        self.async_session.add(instance=new_aimodel)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_aimodel)

        return new_aimodel

    async def read_aimodels(self) -> typing.Sequence[AiModel]:
        stmt = sqlalchemy.select(AiModel)
        query = await self.async_session.execute(statement=stmt)
        return query.scalars().all()

    async def read_aimodel_by_id(self, id: int) -> AiModel:
        stmt = sqlalchemy.select(AiModel).where(AiModel.id == id)
        query = await self.async_session.execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist("Account with id `{id}` does not exist!")

        return query.scalar()  # type: ignore

    async def read_aimodel_by_name(self, name: str) -> AiModel:
        stmt = sqlalchemy.select(AiModel).where(AiModel.name == name)
        query = await self.async_session.execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist("Account with username `{name}` does not exist!")

        return query.scalar()  # type: ignore

    async def update_aimodel_by_id(self, id: int, aicount_update: AiModelInUpdate) -> AiModel:
        new_aicount_data = aicount_update.dict()

        select_stmt = sqlalchemy.select(AiModel).where(AiModel.id == id)
        query = await self.async_session.execute(statement=select_stmt)
        update_aimodel = query.scalar()

        if not update_aimodel:
            raise EntityDoesNotExist(f"AiModel with id `{id}` does not exist!")  # type: ignore

        update_stmt = sqlalchemy.update(table=AiModel).where(AiModel.id == update_aimodel.id).values()  # type: ignore

        if new_aicount_data["name"]:
            update_stmt = update_stmt.values(username=new_aicount_data["name"])

        if new_aicount_data["des"]:
            update_stmt = update_stmt.values(username=new_aicount_data["des"])

        await self.async_session.execute(statement=update_stmt)
        await self.async_session.commit()
        await self.async_session.refresh(instance=update_aimodel)

        return update_aimodel  # type: ignore

    async def delete_account_by_id(self, id: int) -> str:
        select_stmt = sqlalchemy.select(AiModel).where(AiModel.id == id)
        query = await self.async_session.execute(statement=select_stmt)
        delete_aimodel = query.scalar()

        if not delete_aimodel:
            raise EntityDoesNotExist(f"Ai Model with id `{id}` does not exist!")  # type: ignore

        stmt = sqlalchemy.delete(table=AiModel).where(AiModel.id == delete_aimodel.id)

        await self.async_session.execute(statement=stmt)
        await self.async_session.commit()

        return f"Ai Model with id '{id}' is successfully deleted!"
