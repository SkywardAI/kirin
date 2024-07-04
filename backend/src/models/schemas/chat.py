import datetime
from typing import Optional

from pydantic import Field

from src.models.schemas.base import BaseSchemaModel


class ChatInMessage(BaseSchemaModel):
    sessionUuid: Optional[str] = Field(None)
    message: str


class ChatInResponse(BaseSchemaModel):
    sessionUuid: str
    message: str


class Session(BaseSchemaModel):
    sessionUuid: str
    name: str | None
    created_at: datetime.datetime


class ChatHistory(BaseSchemaModel):
    sessionUuid: str
    type: str
    message: str


class MessagesResponse(BaseSchemaModel):
    role: str
    content: str