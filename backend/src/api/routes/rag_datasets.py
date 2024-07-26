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
from src.models.schemas.dataset import RagDatasetCreate, RagDatasetResponse, LoadRAGDSResponse
from src.repository.rag_datasets_eng import DatasetEng
from src.repository.crud.account import AccountCRUDRepository
from src.repository.crud.dataset_db import DataSetCRUDRepository
from src.securities.authorizations.jwt import jwt_required
from src.repository.crud.chat import SessionCRUDRepository
from src.utilities.formatters.ds_formatter import DatasetFormatter
from src.config.manager import settings


router = fastapi.APIRouter(prefix="/ds", tags=["RAG datasets"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/verify")


@router.get(
    path="/list",
    name="datasets:get-dataset-list",
    response_model=list[RagDatasetResponse],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_dataset_list(
    token: str = fastapi.Depends(oauth2_scheme),
    ds_repo: DataSetCRUDRepository = fastapi.Depends(get_repository(repo_type=DataSetCRUDRepository)),
) -> list[RagDatasetResponse]:
    """
    Get all the pre-processed dataset list.

    ```
    curl -X 'GET' \
    'http://127.0.0.1:8000/api/ds/list' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFub255bW91cyIsImVtYWlsIjoiYW5vbnltb3VzQGFub255LmNvbSIsImV4cCI6MTcyMjIyMDUzMiwic3ViIjoiWU9VUi1KV1QtU1VCSkVDVCJ9.S4Y2xvvWmKHlT-OXgrRpO2ycNQcTFOg81J9W3syFekg'
    ```

    Returns:
    
    ```
    [
        {
            "dataset_name": "aisuko/squad01"
        }
    ]
    ```

    """
    # It is unthread safe
    # list_ds_from_db = await ds_repo.get_dataset_list()

    list_ds = [settings.DEFAULT_RAG_DS_NAME]

    return [RagDatasetResponse(dataset_name=ds_name) for ds_name in list_ds]


@router.post(
    path="/load",
    name="datasets:load-dataset",
    response_model=LoadRAGDSResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def load_dataset(
    rag_ds_create: RagDatasetCreate,
    token: str = fastapi.Depends(oauth2_scheme),
    session_repo: SessionCRUDRepository = fastapi.Depends(get_repository(repo_type=SessionCRUDRepository)),
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
    jwt_payload: dict = fastapi.Depends(jwt_required),
) -> LoadRAGDSResponse:
    """

    Loading the specific dataset into the vector db. However here are some requirements:
    * The dataset should be in the format of the RAG dataset. And we define the RAG dataset.
    * Anonymous user can't load the dataset. The user should be authenticated.
    * The dataset related to the specific user's specific session.

    ```
    curl -X 'POST' \
    'http://127.0.0.1:8000/api/ds/load' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFub255bW91cyIsImVtYWlsIjoiYW5vbnltb3VzQGFub255LmNvbSIsImV4cCI6MTcyMjIyMDAxNiwic3ViIjoiWU9VUi1KV1QtU1VCSkVDVCJ9.8JIiQ91Lh10n6N5bWOdb3A_QbCRT5FsCKRwEKXhNsRw' \
    -H 'Content-Type: application/json' \
    -d '{
    "sessionUuid": "0a38c59f-b8fd-4ec4-abd7-581f731aebd7",
    "name": "aisuko/squad01",
    "des": "string",
    "ratio": 0
    }'
    ```

    Returns:
    ```
    {
    "name": "aisuko/squad01",
    "status": true
    }
    ```
    """

    current_user = await account_repo.read_account_by_username(username=jwt_payload.username)
    # Here we don't use async because load_dataset is a sync function in HF ds
    status: bool = True if DatasetEng.load_dataset(rag_ds_create.dataset_name).get("insert_count") > 0 else False

    match status:
        case True:
            await session_repo.append_ds_name_to_session(
                session_uuid=rag_ds_create.sessionUuid,
                account_id=current_user.id,
                ds_name=DatasetFormatter.format_dataset_by_name(
                    rag_ds_create.dataset_name
                ),  # ds_name should be same as collectioname in vector db
            )
        case False:
            return LoadRAGDSResponse(dataset_name=rag_ds_create.dataset_name, status=status)

    return LoadRAGDSResponse(dataset_name=rag_ds_create.dataset_name, status=status)
