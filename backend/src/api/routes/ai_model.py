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

from src.utilities.exceptions.database import EntityDoesNotExist
from src.models.db.ai_model import AiModel
import fastapi

from src.api.dependencies.repository import get_rag_repository, get_repository
from src.models.schemas.ai_model import AiModelCreate, AiModelChooseResponse, AiModelInResponse, AiModelCreateResponse
from src.repository.crud.ai_model import AiModelCRUDRepository
from src.repository.rag.chat import RAGChatModelRepository

router = fastapi.APIRouter(prefix="/models", tags=["model"])


@router.get(
    path="",
    name="models:get-model-list",
    response_model=list[AiModelInResponse],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_aimodels(
    aimodel_repo: AiModelCRUDRepository = fastapi.Depends(get_repository(repo_type=AiModelCRUDRepository)),
) -> list[AiModelInResponse]:
    """
    Get a list of AI models

    This endpoint retrieves all teh AI models available in the system.

    ```bash
    curl -X 'GET' 'http://127.0.0.1:8000/models'
    -H 'accept: application/json'
    ```

    Returns a list of AiModelInResponse objects:
    - **id**: The id of the model
    - **name**: The name of the model
    - **des**: The description of the model
    """
    ai_models = await aimodel_repo.read_aimodels()
    ai_model_list: list = list()

    for ai_model in ai_models:
        aimodel = AiModelInResponse(
            id=ai_model.id,
            name=ai_model.name,
            des=ai_model.des,
        )
        ai_model_list.append(aimodel)

    return ai_model_list


@router.post(
    path="/{id}",
    name="models:choose-model",
    response_model=AiModelChooseResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def choose_aimodels(
    id: int,
    aimodel_repo: AiModelCRUDRepository = fastapi.Depends(get_repository(repo_type=AiModelCRUDRepository)),
    rag_chat_repo: RAGChatModelRepository = fastapi.Depends(get_rag_repository(repo_type=RAGChatModelRepository)),
) -> AiModelChooseResponse:
    """
    Choose an AI model by ID

    This endpoint selects a specific AI model by ID.

    ```bash
    curl -X 'POST' 'http://127.0.0.1:8000/models/{id}'
    -H 'accept: application/json'
    ```

    Returns an AiModelChooseResponse object:
    - **name**: The name of the model
    - **msg**: The message indicating the success or failure of the model selection
    """
    ai_model = await aimodel_repo.read_aimodel_by_id(id=id)
    result = await rag_chat_repo.load_model(session_id=id, model_name=ai_model.name)
    if result:
        return AiModelChooseResponse(
            name=ai_model.name,
            msg="Model has been selected",
        )
    else:
        return AiModelChooseResponse(
            name=ai_model.name,
            msg="Sorry Model init failed! Please try again!",
        )


@router.post(
    path="",
    name="models:create-model",
    response_model=AiModelCreateResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def create_ai_model(
    ai_model: AiModelCreate,
    aimodel_repo: AiModelCRUDRepository = fastapi.Depends(get_repository(repo_type=AiModelCRUDRepository)),
) -> AiModelCreateResponse:
    """
    Create a new AI model

    ```bash
    curl -X 'POST' 'http://127.0.0.1:8000/models'
    -H 'accept: application/json'
    -H 'Content-Type: application/json'
    -d '{
        "name": "knew_bee_model",
        "des": "This model is pretty knew bee"
    }'
    ```

    Returns an AiModelCreateResponse object:
    - **id**: The id of the model
    - **name**: The name of the model
    - **des**: The description of the model
    """
    req_model = AiModel(name=ai_model.name, des=ai_model.des)

    db_model = await aimodel_repo.get_aimodel_by_name(ai_model.name)
    if db_model is not None:
        raise EntityDoesNotExist(f"AiModel with id `{ai_model.name}`   alread exist!")

    ai_model = await aimodel_repo.create_aimodel(aimodel_create=req_model)
    return AiModelCreateResponse(id=ai_model.id, name=ai_model.name, des=ai_model.des)
