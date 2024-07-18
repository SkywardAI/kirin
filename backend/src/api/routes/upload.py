import os

from src.repository.crud.dataset_db import DataSetCRUDRepository
from src.repository.rag.chat import RAGChatModelRepository
from src.securities.authorizations.jwt import jwt_required
import fastapi
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
    file: fastapi.UploadFile = fastapi.File(...),
    rag_chat_repo: RAGChatModelRepository = fastapi.Depends(get_rag_repository(repo_type=RAGChatModelRepository)),
    dataset_repo: DataSetCRUDRepository = fastapi.Depends(get_rag_repository(repo_type=DataSetCRUDRepository)),
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
    token: str = fastapi.Depends(oauth2_scheme),
    jwt_payload: dict = fastapi.Depends(jwt_required),
):
    """
    
    Upload csv file to vectorDB
    
    **Note:**
    
    better have a validation of file name. We don't have limitation of file name yet, it is better to only allow letters and number with '_' in file name

    ```bash

    curl -X 'POST' \
    'http://127.0.0.1:8000/api/upload/file' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFub255bW91cyIsImVtYWlsIjoiYW5vbnltb3VzQGFub255LmNvbSIsImV4cCI6MTcyMTU0NzI3Nywic3ViIjoiWU9VUi1KV1QtU1VCSkVDVCJ9.XqTugA3Lz_4pcE83JjqtB027YIz6U-O2aLxpSqZpBQk' \
    -H 'Content-Type: multipart/form-data' \
    -F 'file=@Sample.csv;type=application/vnd.ms-excel'

    ```
    
    **Returns**

    {
    "ID": 1
    }
    
    """
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
    current_user = await account_repo.read_account_by_username(username=jwt_payload.username)
    db_fileinfo = await dataset_repo.init_dataset(dataset_name=filename, account_id=current_user.id) 

    # Save file
    save_file = os.path.join(save_path, filename)
    if os.path.exists(save_file):
        os.remove(save_file)
    contents = await file.read()
    # Use background task to load file data to vector db
    # background_tasks.add_task(save_upload_file, contents, save_file, filename,db_fileinfo.id, rag_chat_repo, dataset_repo)
    await save_upload_file(contents, save_file, filename,rag_chat_repo)
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
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
    token: str = fastapi.Depends(oauth2_scheme),
    jwt_payload: dict = fastapi.Depends(jwt_required),
):
    """
    
    Upload dataset to vectorDB
    
    **Note:**
    
    Dataset will be downloaded from huggingface. 
    
    We assume the dataset contains embeddings , example is aisuko/RMIT-2024-pd-study-areas. If the dimision of dataset is not 3072, we will pad it with zeros
    
    If the dataset have different structure or no embeddings included , then we cannot save it to vectorDB
    
    ```bash

    curl -X 'POST' \
    'http://127.0.0.1:8000/api/upload/dataset?date_set_name=aisuko%2FRMIT-2024-pd-study-areas' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFub255bW91cyIsImVtYWlsIjoiYW5vbnltb3VzQGFub255LmNvbSIsImV4cCI6MTcyMTU0NzI3Nywic3ViIjoiWU9VUi1KV1QtU1VCSkVDVCJ9.XqTugA3Lz_4pcE83JjqtB027YIz6U-O2aLxpSqZpBQk' \
    -d ''

    ```
    
    **Returns**

    {
    "ID": 1
    }
    
    """
    current_user = await account_repo.read_account_by_username(username=jwt_payload.username)
    db_dataset = await dataset_repo.init_dataset(dataset_name=date_set_name, account_id=current_user.id) 
    # background_tasks.add_task(rag_chat_repo.load_data_set, date_set_name,db_dataset.id,dataset_repo)
    await rag_chat_repo.load_data_set(date_set_name)
    return FileInResponse(ID=db_dataset.id )


# @router.get(
#     "/status/{id}",
#     name="upload:get load status by id",
#     response_model=bool,
#     status_code=fastapi.status.HTTP_200_OK,
# )
# async def get_status(
#     id :int,
#     dataset_repo: DataSetCRUDRepository = fastapi.Depends(get_rag_repository(repo_type=DataSetCRUDRepository)),
# ):
#     """
    
#     Check status for dataset / csv upload ,  return True for loaded successfully , False for not loaded yet or dataset not exists
    
#     ```bash

#     curl -X 'GET' \
#     'http://127.0.0.1:8000/api/upload/status/1' \
#     -H 'accept: application/json'

#     ```
    
#     **Returns**

#     True
    
#     """
#     result = await dataset_repo.get_load_status(id)
#     return result



