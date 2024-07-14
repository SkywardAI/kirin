import os

from src.repository.crud.dataset_db import DataSetCRUDRepository
from src.repository.rag.chat import RAGChatModelRepository
from src.models.schemas.train import TrainFileInResponse
from src.models.schemas.dataset import DatasetCreate
import fastapi
import threading
from fastapi import BackgroundTasks
from src.repository.inference_eng import inference_helper
from src.api.dependencies.repository import get_rag_repository
from src.config.settings.const import UPLOAD_FILE_PATH
from src.models.schemas.file import FileInResponse


router = fastapi.APIRouter(prefix="/upload", tags=["upload"])


async def save_upload_file(contents: bytes, save_file: str, filename: str, rag_chat_repo: RAGChatModelRepository):
    with open(save_file, "wb") as f:
        f.write(contents)
    await rag_chat_repo.load_csv_file(file_name=filename)
    

@router.post(
    "/file",
    name="upload:upload file to vectorDB",
    response_model=FileInResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def upload_and_return_id(
    background_tasks: BackgroundTasks,
    file: fastapi.UploadFile = fastapi.File(...),
    rag_chat_repo: RAGChatModelRepository = fastapi.Depends(get_rag_repository(repo_type=RAGChatModelRepository)),
    dataset_repo: DataSetCRUDRepository = fastapi.Depends(get_rag_repository(repo_type=DataSetCRUDRepository)),
):

    filename=file.filename
    save_path = UPLOAD_FILE_PATH
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    save_file = os.path.join(save_path, filename)
    if os.path.exists(save_file):
        os.remove(save_file)
    db_fileinfo = await dataset_repo.get_dataset_by_name(filename)
    if not db_fileinfo:
        db_fileinfo = await dataset_repo.create_dataset(DatasetCreate(dataset_name=filename,des=filename)) 
    save_file = os.path.join(save_path, filename)
    if os.path.exists(save_file):
        os.remove(save_file)
    contents = await file.read()
    background_tasks.add_task(save_upload_file, contents, save_file, filename, rag_chat_repo)

    return FileInResponse(ID=db_fileinfo.id)

@router.post(
    "/dataset",
    name="upload:load dataset to vectorDB",
    response_model=TrainFileInResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def upload_and_return_id(
    date_set_name: str,
    rag_chat_repo: RAGChatModelRepository = fastapi.Depends(get_rag_repository(repo_type=RAGChatModelRepository)),
    dataset_repo: DataSetCRUDRepository = fastapi.Depends(get_rag_repository(repo_type=DataSetCRUDRepository)),
):

    db_dataset=await dataset_repo.get_dataset_by_name(date_set_name)
    if not db_dataset:
        db_dataset = await dataset_repo.create_dataset(DatasetCreate(dataset_name=date_set_name,des=date_set_name)) 
    dataload_thread = threading.Thread(target=rag_chat_repo.load_data_set,args=(date_set_name,) )
    dataload_thread.daemon = True
    dataload_thread.start()
    return FileInResponse(ID=db_dataset.id )


@router.get(
    "/{id}",
    name="upload:get load status by id",
    response_model=bool,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_status(
    id :str,
    dataset_repo: DataSetCRUDRepository = fastapi.Depends(get_rag_repository(repo_type=DataSetCRUDRepository)),
):

    return dataset_repo.get_load_status(id)


@router.post(
    "/test",
    name="upload:load dataset to vectorDB",
    response_model=list,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def upload_and_return_id(
    text_list: list[str],
):

    return inference_helper.tokenize(text_list)



