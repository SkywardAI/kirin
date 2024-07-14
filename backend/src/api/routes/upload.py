import os

from src.repository.crud.dataset_db import DataSetCRUDRepository
from src.repository.rag.chat import RAGChatModelRepository
from src.models.schemas.train import TrainFileInResponse
from src.models.schemas.dataset import DatasetCreate
import fastapi
import threading
from fastapi import BackgroundTasks
from src.repository.inference_eng import inference_helper
from src.api.dependencies.repository import get_rag_repository, get_repository
from src.config.settings.const import UPLOAD_FILE_PATH
from src.models.schemas.file import FileInResponse
from src.repository.crud.file import UploadedFileCRUDRepository
from src.utilities.exceptions.database import EntityAlreadyExists

from src.utilities.exceptions.http.exc_400 import (
   http_400_exc_bad_file_name_request,
)

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
    file_repo: UploadedFileCRUDRepository = fastapi.Depends(get_repository(repo_type=UploadedFileCRUDRepository)),
):

    filename=file.filename 
    try:
        new_file = await file_repo.create_uploadfile(file_name=filename)
        save_path = UPLOAD_FILE_PATH
    except EntityAlreadyExists:
        raise await http_400_exc_bad_file_name_request(filename)

    if not os.path.exists(save_path):
        os.mkdir(save_path)
    save_file = os.path.join(save_path, filename)
    contents = await file.read()
    background_tasks.add_task(save_upload_file, contents, save_file, filename, rag_chat_repo)

    return FileInResponse(ID=new_file.id)

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
        dataload_thread = threading.Thread(target=rag_chat_repo.load_data_set,args=(date_set_name,) )
        dataload_thread.daemon = True
        dataload_thread.start()
        db_dataset = await dataset_repo.create_dataset(DatasetCreate(dataset_name=date_set_name,des=date_set_name)) 

    return FileInResponse(ID=db_dataset.id )


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



