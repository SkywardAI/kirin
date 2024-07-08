from pydantic import Field
from src.models.schemas.base import BaseSchemaModel


class TrainFileIn(BaseSchemaModel):
    fileID: int | None = Field(..., title="File Id", description="File Id")
    dataSet: str | None = Field(..., title="DataSet", description="DataSet")
    modelID: int | None = Field(..., title="Model id", description="Model id")
    embedField : str | None = Field(..., title="Embed Field", description="Embed Field")
    resField : str | None = Field(..., title="Result Field", description="Result Field")
    directLoad: bool = False


class TrainFileInResponse(BaseSchemaModel):
    trainID: int | None = Field(..., title="TrainID", description="trainID")
    msg : str =Field(..., title="Message", description="Message")
