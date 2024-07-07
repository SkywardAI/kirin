import datetime
from typing import Optional

from pydantic import Field

from src.models.schemas.base import BaseSchemaModel


class ChatInMessage(BaseSchemaModel):
    sessionUuid: Optional[str] | None = Field(..., title="Session UUID", description="Session UUID")
    message: str  = Field(..., title="Message", description="Message")


class ChatInResponse(BaseSchemaModel):
    sessionUuid: str = Field(..., title="Session UUID", description="Session UUID")
    message: str = Field(..., title="Message", description="Message")


class Session(BaseSchemaModel):
    sessionUuid: str = Field(..., title="Session UUID" ,description="Session UUID") 
    name: str | None  = Field(..., title="Name", description="Name") 
    created_at: datetime.datetime = Field(..., title="Creation time", description="Creation time") 


class ChatHistory(BaseSchemaModel):
    sessionUuid: str = Field(..., title="Session UUID", description="Session UUID") 
    type: str  = Field(..., title="Type", description="Type") 
    message: str = Field(..., title="Message", description="Message")


class MessagesResponse(BaseSchemaModel):
    role: str = Field(..., title="Role", description="Role")
    content: str = Field(..., title="Content", description="Content")