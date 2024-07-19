import typing

import sqlalchemy

from src.models.db.ai_model import AiModel
from src.models.schemas.ai_model import AiModelInUpdate
from src.repository.crud.base import BaseCRUDRepository
from src.utilities.exceptions.database import EntityDoesNotExist


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
        result = await self.async_session.execute(statement=stmt)
        ai_model = result.scalar_one_or_none()
        if ai_model is None:
            raise EntityDoesNotExist(f"AiModel with id `{id}` does not exist!")
        return ai_model

    async def read_aimodel_by_name(self, name: str) -> AiModel:
        stmt = sqlalchemy.select(AiModel).where(AiModel.name == name)
        query = await self.async_session.execute(statement=stmt)
        ai_model = query.scalar()
        if ai_model is None:
            raise EntityDoesNotExist(f"AiModel with name `{name}` does not exist!")

        return ai_model

    async def get_aimodel_by_name(self, name: str) -> AiModel:
        stmt = sqlalchemy.select(AiModel).where(AiModel.name == name)
        query = await self.async_session.execute(statement=stmt)
        return query.scalar()

    async def update_aimodel_by_id(self, id: int, aimodel_update: AiModelInUpdate) -> AiModel:
        new_aimodel_data = aimodel_update.dict()

        select_stmt = sqlalchemy.select(AiModel).where(AiModel.id == id)
        query = await self.async_session.execute(statement=select_stmt)
        update_aimodel = query.scalar()

        if not update_aimodel:
            raise EntityDoesNotExist(f"AiModel with id `{id}` does not exist!")

        update_stmt = (
            sqlalchemy.update(AiModel)
            .where(AiModel.id == update_aimodel.id)
            .values(name=new_aimodel_data["name"], des=new_aimodel_data["des"])
        )

        await self.async_session.execute(statement=update_stmt)
        await self.async_session.commit()
        await self.async_session.refresh(instance=update_aimodel)

        return update_aimodel

    async def delete_aimodel_by_id(self, id: int) -> str:
        select_stmt = sqlalchemy.select(AiModel).where(AiModel.id == id)
        query = await self.async_session.execute(statement=select_stmt)
        delete_aimodel = query.scalar()

        if not delete_aimodel:
            raise EntityDoesNotExist(f"AiModel with id `{id}` does not exist!")

        stmt = sqlalchemy.delete(AiModel).where(AiModel.id == delete_aimodel.id)

        await self.async_session.execute(statement=stmt)
        await self.async_session.commit()

        return f"AiModel with id '{id}' is successfully deleted!"
