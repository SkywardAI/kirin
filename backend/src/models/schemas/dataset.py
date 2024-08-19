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

from typing import Optional
import datetime

from pydantic import Field
from src.models.schemas.base import BaseSchemaModel


class DatasetCreate(BaseSchemaModel):
    dataset_name: str = Field(..., title="DataSet Name", description="DataSet Name")
    table_name: str = Field(..., title="Table Name", description="Table Name")
    des: str | None = Field(..., title="Details", description="Details")


class DatasetResponse(BaseSchemaModel):
    id: int = Field(..., title="id", description="id")
    dataset_name: str = Field(..., title="DataSet Name", description="DataSet Name")
    created_at: datetime.datetime | None = Field(..., title="Creation time", description="Creation time")
    updated_at: datetime.datetime | None = Field(..., title="Update  time", description="Update time")


class RagDatasetCreate(BaseSchemaModel):
    sessionUuid: str = Field(..., title="Session UUID", description="Session UUID")
    dataset_name: str = Field(..., title="DataSet Name", description="DataSet Name")
    des: str | None = Field(..., title="Details", description="Details")
    ratio: Optional[float] = Field(..., title="Ratio", description="Ratio")


class RagDatasetResponse(BaseSchemaModel):
    dataset_name: str = Field(..., title="DataSet Name", description="DataSet Name")
    # status: bool = Field(..., title="Status", description="Status")
    # created_at: datetime.datetime | None = Field(..., title="Creation time", description="Creation time")
    # updated_at: datetime.datetime | None = Field(..., title="Update  time", description="Update time")
    # ratio: Optional[float] = Field(..., title="Ratio", description="Ratio")


class LoadRAGDSResponse(BaseSchemaModel):
    dataset_name: str = Field(..., title="DataSet Name", description="DataSet Name")
    status: bool = Field(default=False, title="Status", description="Status")
    # created_at: datetime.datetime | None = Field(..., title="Creation time", description="Creation time")
    # updated_at: datetime.datetime | None = Field(..., title="Update  time", description="Update time")
    # ratio: Optional[float] = Field(..., title="Ratio", description="Ratio")

class DataSet(BaseSchemaModel):  # type: ignore
    uuid: str
    name: str
    account_id: int
    table_name:str
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)