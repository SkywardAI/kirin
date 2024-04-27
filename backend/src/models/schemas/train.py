from src.models.schemas.base import BaseSchemaModel


class TrainFileIn(BaseSchemaModel):
    fileID: int | None = None
    dataSet: str | None = None
    modelID: int | None = None


class TrainFileInResponse(BaseSchemaModel):
    trainID: int | None = None
    msg : str


class TrainStatusInResponse(BaseSchemaModel):
    status: int | None = None
    msg : str
