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
from src.models.schemas.dataset import RagDatasetCreate, RagDatasetResponse, LoadRAGDSResponse, DatasetCreate
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
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
    jwt_payload: dict = fastapi.Depends(jwt_required),
) -> list[RagDatasetResponse]:
    """
    Get all the pre-processed dataset list for admin users
    Get dataset list for the specific user

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
            "dataset_name": "aisuko/squad01-v2"
        }
    ]
    ```

    """
    current_user = account_repo.read_account_by_username(username=jwt_payload.username)
    account_id=current_user.id
    if current_user.username == settings.ADMIN_USERNAME: 
        list_ds = ds_repo.get_dataset_list()
    else:
        list_ds = ds_repo.get_dataset_list_by_account_id(account_id=account_id)
    if not list_ds:
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
    background_tasks: fastapi.BackgroundTasks,
    token: str = fastapi.Depends(oauth2_scheme),
    session_repo: SessionCRUDRepository = fastapi.Depends(get_repository(repo_type=SessionCRUDRepository)),
    ds_repo: DataSetCRUDRepository = fastapi.Depends(get_repository(repo_type=DataSetCRUDRepository)),
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
    "name": "aisuko/squad01-v2",
    "des": "string",
    "ratio": 0
    }'
    ```

    Returns:
    ```
    {
    "name": "aisuko/squad01-v2",
    "status": true
    }
    ```
    """
    current_user = account_repo.read_account_by_username(username=jwt_payload.username)
    # Here we don't use async because load_dataset is a sync function in HF ds
    # status: bool = True if DatasetEng.load_dataset(rag_ds_create.dataset_name).get("insert_count") > 0 else False
    session = session_repo.read_create_sessions_by_uuid(
        session_uuid=rag_ds_create.sessionUuid, account_id=current_user.id, name="new session", session_type="rag"
    )
    try:
        # Here we use async because we need to update the session db
        dataset_list = DatasetEng.validate_dataset(rag_ds_create.dataset_name)
        status: bool =True
    except Exception:
        status: bool = False

    async def load_dataset_task(dataset_name: str, ds_list: list):
        DatasetEng.load_dataset(dataset_name, ds_list)
    match status:
        case True:
            table_name = DatasetFormatter.format_dataset_by_name(
                    rag_ds_create.dataset_name
                )
            session_repo.append_ds_name_to_session(
                session_uuid=session.session_uuid,
                account_id=current_user.id,
                ds_name=table_name,  # ds_name should be same as collectioname in vector db
            )
            ds_repo.create_datasset(account_id=current_user.id, dataset_create=DatasetCreate(
                dataset_name=rag_ds_create.dataset_name,
                table_name=table_name,
                des=""
            ))
            background_tasks.add_task(load_dataset_task, rag_ds_create.dataset_name, dataset_list)
        case False:
            return LoadRAGDSResponse(dataset_name=rag_ds_create.dataset_name, session_uuid=session.session_uuid, status=status)

    return LoadRAGDSResponse(dataset_name=rag_ds_create.dataset_name, session_uuid=session.session_uuid, status=status)
