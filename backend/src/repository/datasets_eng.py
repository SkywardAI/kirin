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

from datasets import load_dataset
from src.repository.vector_database import vector_db


class DatasetEng:
    def __init__(self):
        pass

    def get_dataset_list(self):
        pass

    def get_dataset_by_name(self, name: str):
        pass

    @classmethod
    async def load_dataset(cls, name: str) -> dict:
        """
        Load dataset from the given name, must connect to the internet

        No need to consider the memory usage
        """

        ds = load_dataset(name)
        ds_list = ds.to_list()

        await vector_db.create_collection(collection_name=name)

        return await vector_db.insert_list(collection_name=name, data_list=ds_list)
