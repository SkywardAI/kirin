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

from src.repository.crud.base import BaseCRUDRepository
from src.models.schemas.dataset import DatasetCreate
from src.models.db.dataset import DataSet
import sqlalchemy

import typing


class DataSetCRUDRepository(BaseCRUDRepository):
    async def create_dataset(self, dataset_create: DatasetCreate) -> DataSet:
        new_dataset = DataSet(name=dataset_create.dataset_name)

        self.async_session.add(instance=new_dataset)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_dataset)

        return new_dataset

    async def get_dataset_by_name(self, dataset_name: str) -> typing.Sequence[DataSet]:
        stmt = sqlalchemy.select(DataSet).where(DataSet.name == dataset_name)
        query = await self.async_session.execute(statement=stmt)
        return query.scalars().all()

    async def get_dataset_list(self) -> typing.Sequence[DataSet]:
        stmt = sqlalchemy.select(DataSet).order_by(DataSet.updated_at.desc())
        query = await self.async_session.execute(statement=stmt)
        return query.scalars().all()
