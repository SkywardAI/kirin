from src.repository.crud.base import BaseCRUDRepository
from sqlalchemy.sql import functions as sqlalchemy_functions
from src.utilities.exceptions.database import EntityDoesNotExist
from src.models.db.dataset import DataSet
import sqlalchemy
import asyncio
from sqlalchemy.exc import TimeoutError

import typing
class DataSetCRUDRepository(BaseCRUDRepository):

    async def init_dataset(self, dataset_name:str, account_id: str) -> DataSet:
        stmt = sqlalchemy.select(DataSet).where(DataSet.name == dataset_name, DataSet.account_id == account_id)
        result = await self.async_session.execute(statement=stmt)
        dataset = result.scalars().first()
        
        if dataset is None:
            dataset=DataSet(name=dataset_name, account_id=account_id)
            self.async_session.add(instance=dataset)
            await self.async_session.commit()
            await self.async_session.refresh(instance=dataset)
        return dataset

    async def mark_loaded(self, id: int)->typing.Sequence[DataSet]:
        update_stmt = sqlalchemy.update(table=DataSet).where(DataSet.id == id).values(updated_at=sqlalchemy_functions.now())  # type: ignore
        update_stmt = update_stmt.values(is_uploaded=True)
        await self.async_session.execute(statement=update_stmt)
        await self.async_session.commit()
        
    async def get_dataset_by_account_id(self, account_id: int) -> DataSet:
        stmt = sqlalchemy.select(DataSet).where(DataSet.account_id == account_id, DataSet.is_uploaded).order_by(DataSet.created_at.desc())
        result = await self.async_session.execute(statement=stmt)
        dataset = result.scalars().first()
        if dataset is None:
            raise EntityDoesNotExist("Dataset for account id `{id}` does not exist!")

        return dataset

    async def get_dataset_by_id(self, id: int) -> DataSet:
        stmt = sqlalchemy.select(DataSet).where(DataSet.id == id, DataSet.is_uploaded)
        query = await self.async_session.execute(statement=stmt)
        dataset = query.scalar()
        if dataset is None:
            raise EntityDoesNotExist("Dataset with id `{id}` does not exist!")

        return dataset
    
    async def get_load_status(self, id: int)->bool:
        try:
            result = await asyncio.wait_for(self.async_session.execute(sqlalchemy.select(DataSet).where(DataSet.id == id)), 5)
            query = result.first()
            if query is None:
                return False
            dataset = query.scalar()
            return dataset.is_uploaded
        except asyncio.TimeoutError:
            await self.async_session.rollback()
            return False
        except TimeoutError:
            await self.async_session.rollback()
            return False
        finally:
            await self.async_session.close()


    async def get_dataset_list(self)->typing.Sequence[DataSet]:
         stmt = sqlalchemy.select(DataSet).order_by(DataSet.updated_at.desc())
         query = await self.async_session.execute(statement=stmt) 
         return query.scalars().all()


