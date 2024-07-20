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
    des: str | None = Field(..., title="Details", description="Details")


class DatasetResponse(BaseSchemaModel):
    id: int = Field(..., title="id", description="id")
    dataset_name: str = Field(..., title="DataSet Name", description="DataSet Name")
    created_at: datetime.datetime | None = Field(..., title="Creation time", description="Creation time")
    updated_at: datetime.datetime | None = Field(..., title="Update  time", description="Update time")


class RagDatasetCreate(BaseSchemaModel):
    name: str = Field(..., title="DataSet Name", description="DataSet Name")
    des: str | None = Field(..., title="Details", description="Details")
    ratio: Optional[float] = Field(..., title="Ratio", description="Ratio")

class RagDatasetResponse(BaseSchemaModel):
    name: str = Field(..., title="DataSet Name", description="DataSet Name")
    # created_at: datetime.datetime | None = Field(..., title="Creation time", description="Creation time")
    # updated_at: datetime.datetime | None = Field(..., title="Update  time", description="Update time")
    # ratio: Optional[float] = Field(..., title="Ratio", description="Ratio")
    status: Optional[str] = Field(..., title="Status", description="Status")