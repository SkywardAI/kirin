import random

import fastapi

from src.api.dependencies.repository import get_repository
from src.models.schemas.train import TrainFileIn, TrainFileInResponse, TrainStatusInResponse

router = fastapi.APIRouter(prefix="/train", tags=["train"])


@router.post(
    "",
    name="train:train-with-file",
    response_model=TrainFileInResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def train(
    train_in_msg: TrainFileIn,
) -> TrainFileInResponse:
    # TODO start process the file with model
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
