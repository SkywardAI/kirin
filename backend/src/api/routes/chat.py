import uuid

import fastapi

from src.api.dependencies.repository import get_repository
from src.models.schemas.chat import ChatInMessage, ChatInResponse
from src.securities.authorizations.jwt import jwt_generator
from src.utilities.exceptions.database import EntityAlreadyExists

router = fastapi.APIRouter(prefix="/chat", tags=["chatbot"])


@router.post(
    "",
    name="chat:chatbot",
    response_model=ChatInResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def chat(
    chat_in_msg: ChatInMessage,
) -> ChatInResponse:
    if not hasattr(chat_in_msg, "sessionId") or not chat_in_msg.sessionId:
        generated_session_id = str(uuid.uuid4())
    else:
        generated_session_id = chat_in_msg.sessionId
    # TODO use RAG framework to generate the response message
    return ChatInResponse(
        sessionId=generated_session_id,
        message=chat_in_msg.message,
    )
