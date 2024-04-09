import os
import random

import fastapi
from fastapi import BackgroundTasks

from src.api.dependencies.repository import get_repository
from src.config.settings.const import UPLOAD_FILE_PATH
from src.models.schemas.file import FileInResponse, FileStatusInResponse
from src.repository.crud.file import UploadedFileCRUDRepository
from src.utilities.exceptions.database import EntityAlreadyExists

from src.utilities.exceptions.http.exc_400 import (
   http_400_exc_bad_file_name_request,
)

router = fastapi.APIRouter(prefix="/file", tags=["file"])


async def save_upload_file(contents: bytes, save_file: str):
    with open(save_file, "wb") as f:
        f.write(contents)


@router.post(
    "",
    name="file:upload file",
    response_model=FileInResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def upload_and_return_id(
    background_tasks: BackgroundTasks,
    file: fastapi.UploadFile = fastapi.File(...),
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
    background_tasks.add_task(save_upload_file, contents, save_file)

    return FileInResponse(fileID=new_file.id)

@router.get(
    path="/dataset",
    name="dataset:get-dataset-list",
    response_model=list[str],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_dataset(
) -> list[str]:
    #TODO return the names of recently used dataset order by last used time desc
    res = ["dataset1","dataset2"]

    return res

@router.get(
    path="/{id}",
    name="file:check upload status",
    response_model=FileStatusInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def check_status(
    id: int,
) -> FileStatusInResponse:

    # TODO check process status of training
    choices = [0, 1, -1]
    # 0 for in process
    # 1 for complete successfully
    # -1 for error
    return FileStatusInResponse(status=1)

