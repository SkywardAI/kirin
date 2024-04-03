from src.models.schemas.base import BaseSchemaModel


class TrainFileIn(BaseSchemaModel):
    fileID: int
    modelID: int


class TrainFileInResponse(BaseSchemaModel):
    trainID: int


class TrainStatusInResponse(BaseSchemaModel):
    status: int
