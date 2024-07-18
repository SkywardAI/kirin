from pydantic import Field
from src.models.schemas.base import BaseSchemaModel


class UploadedFile(BaseSchemaModel):
    name: str = Field(..., title="name", description="name")


class FileInResponse(BaseSchemaModel):
    ID: int = Field(..., title="file Id", description="file Id")
