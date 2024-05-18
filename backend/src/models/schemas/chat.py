import datetime
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
    accuracy: float


class Session(BaseSchemaModel):
    id: int
    name: str | None
    created_at: datetime.datetime


class ChatHistory(BaseSchemaModel):
    id: int
    type: str
    message: str


class MessagesResponse(BaseSchemaModel):
    role: str
    content: str