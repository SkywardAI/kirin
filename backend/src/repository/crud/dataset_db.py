


from src.repository.crud.base import BaseCRUDRepository
from src.models.schemas.dataset import DatasetCreate
from src.models.db.dataset import DataSet
import sqlalchemy
from sqlalchemy import desc

import typing
class DataSetCRUDRepository(BaseCRUDRepository):
  
    async def create_dataset(self, dataset_create: DatasetCreate) -> DataSet:
        new_dataset=DataSet(name=dataset_create.dataset_name)

        self.async_session.add(instance=new_dataset)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_dataset)

        return new_dataset


      
    async def get_dataset_by_name(self,dataset_name: str)->typing.Sequence[DataSet]:
         stmt = sqlalchemy.select(DataSet).where(DataSet.name == dataset_name)
         query = await self.async_session.execute(statement=stmt) 
         return query.scalars().all()
    


    async def get_dataset_list(self)->typing.Sequence[DataSet]:
         stmt = sqlalchemy.select(DataSet).order_by(DataSet.updated_at.desc())
         query = await self.async_session.execute(statement=stmt) 
         return query.scalars().all()


