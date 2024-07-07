from typing import Optional

from pydantic import Field
from src.models.schemas.base import BaseSchemaModel


class AiModelCreate(BaseSchemaModel):
    # id: int | None
    name: str = Field(..., title="Model Name", description="Model Name")
    des: str = Field(..., title="Details", description="Details")

class AiModelCreateResponse(BaseSchemaModel):
    id: int = Field(..., title="id", description="id")
    name: str = Field(..., title="name", description="name")
    des: str = Field(..., title="Details", description="Details")
    msg: Optional[str] = None

class AiModelInResponse(BaseSchemaModel):
    id: int = Field(..., title="id", description="id")
    name: str = Field(..., title="name", description="name")
    des: str = Field(..., title="Details", description="Details")


class AiModelInUpdate(BaseSchemaModel):
    name: str = Field(..., title="name", description="name")
    des: str = Field(..., title="Details", description="Details")


class AiModelChooseResponse(BaseSchemaModel):
    name: str = Field(..., title="name", description="name")
    msg: str = Field(..., title="Details", description="Details")
