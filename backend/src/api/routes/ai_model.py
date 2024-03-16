import fastapi

from src.api.dependencies.repository import get_repository
from src.models.schemas.ai_model import AiModel, AiModelInResponse
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
            available_models=AiModel(
                name=ai_model.name,
                des=ai_model.des,
            ),
        )
        ai_model_list.append(aimodel)

    return ai_model_list
