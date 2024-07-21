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
from src.models.schemas.dataset import RagDatasetCreate, RagDatasetResponse
from src.repository.rag_datasets_eng import DatasetEng

router = fastapi.APIRouter(prefix="/ds", tags=["datasets"])


@router.get(
    path="/list",
    name="datasets:get-dataset-list",
    response_model=list[RagDatasetResponse],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_dataset_list() -> list[RagDatasetResponse]:
    """
    Waiting for implementing

    """
    pass


@router.get(
    path="/{name}",
    name="datasets:get-dataset-by-name",
    response_model=RagDatasetResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_dataset_by_name(name: str) -> RagDatasetResponse:
    """
    Waiting for implementing
    """
    pass


@router.post(
    path="/load",
    name="datasets:load-dataset",
    response_model=RagDatasetResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def load_dataset(
    rag_ds_create: RagDatasetCreate,
) -> RagDatasetResponse:
    """

    Loading the specific dataset into the vector db

    curl -X 'POST' \
    'http://127.0.0.1:8000/api/ds/load' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "name": "aisuko/squad01",
    "des": "string",
    "ratio": 0
    }'

    Return:
    {
    "name": "aisuko/squad01",
    "status": "Success"
    }
    """

    res: dict = DatasetEng.load_dataset(rag_ds_create.name)

    if res.get("insert_count") > 0:
        status = "Success"
    else:
        status = "Failed"

    return RagDatasetResponse(name=rag_ds_create.name, status=status)
