from typing import Optional

from pydantic import Field

from src.models.schemas.base import BaseSchemaModel


class ChatInMessage(BaseSchemaModel):
    accountID: Optional[int] = Field(None)
    sessionId: Optional[int] = Field(None)
    message: str


class ChatInResponse(BaseSchemaModel):
    sessionId: int
    message: str


class Session(BaseSchemaModel):
    id: int
    name: str | None


class ChatHistory(BaseSchemaModel):
    id: int
    type: str
    message: str
