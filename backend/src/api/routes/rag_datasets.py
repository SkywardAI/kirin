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
from fastapi.security import OAuth2PasswordBearer

from src.api.dependencies.repository import get_repository
from src.models.schemas.dataset import RagDatasetCreate, RagDatasetResponse
from src.repository.rag_datasets_eng import DatasetEng
from src.repository.crud.account import AccountCRUDRepository
from src.securities.authorizations.jwt import jwt_required
from src.repository.crud.chat import SessionCRUDRepository


router = fastapi.APIRouter(prefix="/ds", tags=["datasets"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/verify")


@router.get(
    path="/list",
    name="datasets:get-dataset-list",
    response_model=list[RagDatasetResponse],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_dataset_list() -> list[RagDatasetResponse]:
    """
    Get all the dataset list by using user's ID from pg

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
    Get the dataset by using the dataset name and user's ID from pg
    """
    pass


@router.post(
    path="/load",
    name="datasets:load-dataset",
    response_model=RagDatasetResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def load_dataset(
    rag_ds_create: RagDatasetCreate,
    token: str = fastapi.Depends(oauth2_scheme),
    session_repo: SessionCRUDRepository = fastapi.Depends(get_repository(repo_type=SessionCRUDRepository)),
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
    jwt_payload: dict = fastapi.Depends(jwt_required),
) -> RagDatasetResponse:
    """
    TODO: need to update

    Loading the specific dataset into the vector db. However here are some requirements:
    * The dataset should be in the format of the RAG dataset. And we define the RAG dataset.
    * Anonymous user can't load the dataset. The user should be authenticated.
    * The dataset related to the specific user's specific session.

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

    # TODO: we can't get session when loading dataset
    res: dict = DatasetEng.load_dataset(rag_ds_create.name)

    if res.get("insert_count") > 0:
        status = "Success"
    else:
        status = "Failed"

    # TODO: Save the ds to the db

    # TODO: save dataset name to the session

    # TODO If we bounding ds to specific user's session, we should upadte ds name to the session and return the session
    return RagDatasetResponse(name=rag_ds_create.name, status=status)
