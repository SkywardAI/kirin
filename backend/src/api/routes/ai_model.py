from src.utilities.exceptions.database import EntityDoesNotExist
from src.models.db.ai_model import AiModel
import fastapi

from src.api.dependencies.repository import get_rag_repository, get_repository
from src.models.schemas.ai_model import AiModelCreate, AiModelChooseResponse, AiModelInResponse,AiModelCreateResponse
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
    req_model= AiModel(name=ai_model.name,des=ai_model.des)

    db_model=await aimodel_repo.get_aimodel_by_name(ai_model.name)
    if db_model is not None:
        raise EntityDoesNotExist(f"AiModel with id `{ai_model.name}`   alread exist!")
       
    ai_model = await aimodel_repo.create_aimodel(aimodel_create=req_model)
    return AiModelCreateResponse(
        id=ai_model.id,
        name=ai_model.name,
        des=ai_model.des
    )