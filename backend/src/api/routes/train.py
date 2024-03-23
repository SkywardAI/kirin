import random

import fastapi

from src.api.dependencies.repository import get_rag_repository, get_repository
from src.models.schemas.train import TrainFileIn, TrainFileInResponse, TrainStatusInResponse
from src.repository.crud.ai_model import AiModelCRUDRepository
from src.repository.crud.file import UploadedFileCRUDRepository
from src.repository.rag.chat import RAGChatModelRepository

router = fastapi.APIRouter(prefix="/train", tags=["train"])


@router.post(
    "",
    name="train:train-with-file",
    response_model=TrainFileInResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def train(
    train_in_msg: TrainFileIn,
    aimodel_repo: AiModelCRUDRepository = fastapi.Depends(get_repository(repo_type=AiModelCRUDRepository)),
    file_repo: UploadedFileCRUDRepository = fastapi.Depends(get_repository(repo_type=UploadedFileCRUDRepository)),
    rag_chat_repo: RAGChatModelRepository = fastapi.Depends(get_rag_repository(repo_type=RAGChatModelRepository)),
) -> TrainFileInResponse:

    ai_model = await aimodel_repo.read_aimodel_by_id(id=train_in_msg.modelID)
    file_csv = await file_repo.read_uploadedfiles_by_id(id=train_in_msg.fileID)

    await rag_chat_repo.load_csv_file(file_name=file_csv.name, model_name=ai_model.name)

    return TrainFileInResponse(
        trainID=train_in_msg.fileID + train_in_msg.modelID,
    )


@router.get(
    path="/{id}",
    name="train:check status",
    response_model=TrainStatusInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def check_status(
    id: int,
) -> TrainStatusInResponse:

    choices = [0, 1, -1]
    # 0 for in process
    # 1 for complete successfully
    # -1 for error
    return TrainStatusInResponse(status=1)
