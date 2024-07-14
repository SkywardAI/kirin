import os

from src.repository.crud.dataset_db import DataSetCRUDRepository
from src.repository.rag.chat import RAGChatModelRepository
from src.securities.authorizations.jwt import jwt_required
from src.models.schemas.dataset import DatasetCreate
import fastapi
import threading
from fastapi import BackgroundTasks
from src.repository.inference_eng import inference_helper
from src.api.dependencies.repository import get_rag_repository, get_repository
from src.config.settings.const import UPLOAD_FILE_PATH
from src.models.schemas.file import FileInResponse
from fastapi.security import OAuth2PasswordBearer
from src.repository.crud.account import AccountCRUDRepository

router = fastapi.APIRouter(prefix="/upload", tags=["upload"])
# Automatically get the token from the request header for Swagger UI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/verify")

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
async def upload_csv_and_return_id(
    background_tasks: BackgroundTasks,
    file: fastapi.UploadFile = fastapi.File(...),
    rag_chat_repo: RAGChatModelRepository = fastapi.Depends(get_rag_repository(repo_type=RAGChatModelRepository)),
    dataset_repo: DataSetCRUDRepository = fastapi.Depends(get_rag_repository(repo_type=DataSetCRUDRepository)),
    token: str = fastapi.Depends(oauth2_scheme),
    jwt_payload: dict = fastapi.Depends(jwt_required),
):
    # If file storage path exists
    filename=file.filename
    save_path = UPLOAD_FILE_PATH
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    save_file = os.path.join(save_path, filename)
    # If the file already exists, delete it
    if os.path.exists(save_file):
        os.remove(save_file)
    # Save file info
    db_fileinfo = await dataset_repo.init_dataset(dataset_name=filename, account_username=jwt_payload.username) 

    # Save file
    save_file = os.path.join(save_path, filename)
    if os.path.exists(save_file):
        os.remove(save_file)
    contents = await file.read()
    # Use background task to load file data to vector db
    background_tasks.add_task(save_upload_file, contents, save_file, filename, rag_chat_repo)

    print(db_fileinfo.id)
    return FileInResponse(ID=db_fileinfo.id)

@router.post(
    "/dataset",
    name="upload:load dataset to vectorDB",
    response_model=FileInResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def upload_dataset_and_return_id(
    date_set_name: str,
    rag_chat_repo: RAGChatModelRepository = fastapi.Depends(get_rag_repository(repo_type=RAGChatModelRepository)),
    dataset_repo: DataSetCRUDRepository = fastapi.Depends(get_rag_repository(repo_type=DataSetCRUDRepository)),
    token: str = fastapi.Depends(oauth2_scheme),
    jwt_payload: dict = fastapi.Depends(jwt_required),
):

    db_dataset = await dataset_repo.init_dataset(dataset_name=date_set_name, account_username=jwt_payload.username) 
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



