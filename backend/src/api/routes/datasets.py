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

import fastapi
from src.models.schemas.dataset import DatasetResponse

router = fastapi.APIRouter(prefix="/ds", tags=["datasets"])


@router.get(
    path="/list",
    name="datasets:get-dataset-list",
    response_model=DatasetResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_dataset_list() -> list[DatasetResponse]:
    pass


@router.get(
    path="/{name}",
    name="datasets:get-dataset-by-name",
    response_model=DatasetResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_dataset_by_name(name: str) -> DatasetResponse:
    pass


@router.post(
    path="/{name}",
    name="datasets:create-dataset",
    response_model=DatasetResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def load_dataset(name: str) -> bool:
    pass
