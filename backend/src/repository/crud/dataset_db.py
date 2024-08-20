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
import lancedb
import loguru
import uuid
from datetime import datetime
from src.config.settings.const import META_LANCEDB
from src.repository.crud.base import BaseCRUDRepository
from src.models.schemas.dataset import DatasetCreate, DataSet
from src.utilities.exceptions.database import EntityDoesNotExist


class DataSetCRUDRepository(BaseCRUDRepository):
    def __init__(self):
        self.db = lancedb.connect(META_LANCEDB)
        self.tbl = self.db.open_table("data_set")
        
    def create_datasset(self,account_id: int, dataset_create: DatasetCreate) -> DataSet:
        try:
            data_set = self.tbl.search().where(f"name = '{dataset_create.name}', account_id = {account_id}", prefilter=True).limit(1).to_list()[0]
        except Exception :
            uuid_id=str(uuid.uuid4())
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.tbl.add([{
            "uuid": uuid_id,
            "name": dataset_create.dataset_name,
            "table_name": dataset_create.table_name,
            "account_id": account_id,
            "created_at": current_time,
            "updated_at": current_time
            }])
            new_dataset = self.tbl.search().where(f"uuid = '{uuid_id}'", prefilter=True).limit(1).to_list()[0]
            loguru.logger.info(f"Dataset not exist , new {dataset_create.dataset_name} saved ")
            return DataSet.from_dict(new_dataset)
        loguru.logger.info(f"Dataset {dataset_create.dataset_name} exist")
        return DataSet.from_dict(data_set)

    def get_dataset_by_name(self, dataset_name: str) -> DataSet:
        try:
            data_set = self.tbl.search().where(f"name = '{dataset_name}'", prefilter=True).limit(1).to_list()[0]
        except Exception as e:
            loguru.logger.error(f"{e}")
            raise EntityDoesNotExist("Dataset with name `{dataset_name}` does not exist!")
        loguru.logger.info(f"Read dataset {dataset_name}")
        return DataSet.from_dict(data_set)

    def update_dataset_time(self, dataset_name: str) -> DataSet:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.tbl.update(where=f"name = '{dataset_name}'", values={"updated_at": current_time})
        except Exception as e:
            loguru.logger.error(f"{e}")
            raise EntityDoesNotExist("Dataset with name `{dataset_name}` does not exist!")
        loguru.logger.info(f"Update dataset {dataset_name}")
        updated_dateset = self.tbl.search().where(f"name = '{dataset_name}'", prefilter=True).limit(1).to_list()[0]
        return DataSet.from_dict(updated_dateset)

    def get_dataset_list(self) -> list[DataSet]:
        loguru.logger.info("Read all dataset")
        dataset_dict_list = self.tbl.search().to_list()
        return [DataSet.from_dict(dataset_dict) for dataset_dict in dataset_dict_list]

    def get_dataset_list_by_account_id(self, account_id: int) -> list[DataSet]:
        loguru.logger.info("Read all dataset")
        dataset_dict_list = self.tbl.search().where(f"account_id = {account_id}", prefilter=True).to_list()
        return [DataSet.from_dict(dataset_dict) for dataset_dict in dataset_dict_list]
