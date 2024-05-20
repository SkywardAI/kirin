import random

from src.models.schemas.dataset import DatasetCreate
from src.repository.crud.dataset_db import DataSetCRUDRepository
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
    dataset_repo: DataSetCRUDRepository = fastapi.Depends(get_rag_repository(repo_type=DataSetCRUDRepository)),
) -> TrainFileInResponse:
    #TODO train can be performed by csv file or dataset
    # 1, either fileID or dataset should be shown in input
    # 2, validate fileID or dataset
    # 3, use file and or dataset perform the training logic (csv id done)

     if  train_in_msg.modelID is not None:  
       ai_model = await aimodel_repo.read_aimodel_by_id(id=train_in_msg.modelID)
       file_csv = await file_repo.read_uploadedfiles_by_id(id=train_in_msg.fileID)
       await rag_chat_repo.load_csv_file(file_name=file_csv.name, model_name=ai_model.name)
     else:
       db_dataset=await dataset_repo.get_dataset_by_name(train_in_msg.dataSet)
       if not db_dataset:
        await rag_chat_repo.load_data_set(train_in_msg) 
        await dataset_repo.create_dataset(DatasetCreate(dataset_name=train_in_msg.dataSet,des=train_in_msg.dataSet)) 

     return TrainFileInResponse(
        msg="successful",
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
