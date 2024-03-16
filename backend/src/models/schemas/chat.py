from typing import Optional

from pydantic import Field

from src.models.schemas.base import BaseSchemaModel


class ChatInMessage(BaseSchemaModel):
    sessionId: Optional[str] = Field(None)
    message: str


class ChatInResponse(BaseSchemaModel):
    sessionId: str
    message: str
