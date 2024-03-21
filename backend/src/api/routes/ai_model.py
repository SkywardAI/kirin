import fastapi

from src.api.dependencies.repository import get_repository
from src.models.schemas.ai_model import AiModel, AiModelChooseResponse, AiModelInResponse
from src.repository.crud.ai_model import AiModelCRUDRepository

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
) -> AiModelChooseResponse:
    ai_model = await aimodel_repo.read_aimodel_by_id(id=id)
    return AiModelChooseResponse(
        name=ai_model.name,
        msg="Model has been selected",
    )
