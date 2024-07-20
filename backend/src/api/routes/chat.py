# coding=utf-8

# Copyright [2024] [SkywardAI]
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import fastapi
import loguru
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import StreamingResponse
from starlette.responses import ContentStream
from src.api.dependencies.repository import get_rag_repository, get_repository
from src.securities.authorizations.jwt import jwt_required
from src.utilities.exceptions.database import EntityDoesNotExist
from src.utilities.exceptions.http.exc_404 import http_404_exc_uuid_not_found_request
from src.config.settings.const import ANONYMOUS_USER
from src.models.schemas.chat import (
    ChatsWithTime,
    ChatInMessage,
    ChatInResponse,
    SessionUpdate,
    Session,
    ChatUUIDResponse,
    SaveChatHistory,
)
from src.repository.crud.chat import ChatHistoryCRUDRepository, SessionCRUDRepository
from src.repository.crud.account import AccountCRUDRepository
from src.repository.rag.chat import RAGChatModelRepository

router = fastapi.APIRouter(prefix="/chat", tags=["chatbot"])
# Automatically get the token from the request header for Swagger UI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/verify")


@router.patch(
    path="/session",
    name="Session:update-session-by-uuid",
    response_model=ChatUUIDResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def update_session(
    token: str = fastapi.Depends(oauth2_scheme),
    session_info: SessionUpdate = fastapi.Body(...),
    session_repo: SessionCRUDRepository = fastapi.Depends(get_repository(repo_type=SessionCRUDRepository)),
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
    jwt_payload: dict = fastapi.Depends(jwt_required),
) -> ChatUUIDResponse:
    """
    update session info by session uuid

    **Example**
    
    ```bash
    curl -X 'PATCH' \
    'http://127.0.0.1:8000/api/chat/session' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFiYyIsImVtYWlsIjoidXNlckBleGFtcGxlLmNvbSIsImV4cCI6MTcyMTIwOTMwOSwic3ViIjoiWU9VUi1KV1QtU1VCSkVDVCJ9.DxotlAw8ZrDlvU8wsDKd2lhuRdwC1-bkcS8kGVZzS04' \
    -H 'Content-Type: application/json' \
    -d '{
    "sessionUuid": "a6348e9d-d5a7-43f8-9ed3-4919f5ba9c0a",
    "name": "new session name",
    "type": "rag"
    }'
    ```
    **Note:**
    name and type are optional. If you don't want to update, just ignore it.
    only rag and chat are allowed for type
    
    **Returns**

    {"sessionUuid": "3917151c-173b-4a9e-92aa-ac1d633472d2"}

    """
    current_user = await account_repo.read_account_by_username(username=jwt_payload.username)
    try:
        sessions = await session_repo.update_sessions_by_uuid(session=session_info, account_id=current_user.id)

    except EntityDoesNotExist:
        raise await http_404_exc_uuid_not_found_request(uuid=session_info.sessionUuid)
    return ChatUUIDResponse(sessionUuid=sessions.uuid)


@router.get(
    "/seesionuuid",
    name="chat:session-uuid",
    response_model=ChatUUIDResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def chat_uuid(
    token: str = fastapi.Depends(oauth2_scheme),
    session_repo: SessionCRUDRepository = fastapi.Depends(get_repository(repo_type=SessionCRUDRepository)),
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
    jwt_payload: dict = fastapi.Depends(jwt_required),
) -> ChatUUIDResponse:
    """
    Create a new session for the current user.
    
    **Example**

    ```bash
    curl -X 'POST' 'http://127.0.0.1:8000/api/chat/seesionuuid'
    -H 'accept: application/json' 
    -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFub255bW91cyIsImVtYWlsIjoiYW5vbnltb3VzQGFub255LmNvbSIsImV4cCI6MTcyMDkxNTQyNywic3ViIjoiWU9VUi1KV1QtU1VCSkVDVCJ9.Utz79iCaFC_OVrS5SUEdvlj2iuWNOSNPoNglFh8tdzI' \
    -d ''
    ```

    **Returns**

    {"sessionUuid": "3917151c-173b-4a9e-92aa-ac1d633472d2"}

    """

    # multiple await keyword will caused the error
    current_user = await account_repo.read_account_by_username(username=jwt_payload.username)
    new_session = await session_repo.create_session(account_id=current_user.id, name="new session")
    session_uuid = new_session.uuid

    return ChatUUIDResponse(sessionUuid=session_uuid)


@router.post(
    "",
    name="chat:chatbot",
    response_model=ChatInResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def chat(
    chat_in_msg: ChatInMessage,
    token: str = fastapi.Depends(oauth2_scheme),
    session_repo: SessionCRUDRepository = fastapi.Depends(get_repository(repo_type=SessionCRUDRepository)),
    rag_chat_repo: RAGChatModelRepository = fastapi.Depends(get_rag_repository(repo_type=RAGChatModelRepository)),
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
    jwt_payload: dict = fastapi.Depends(jwt_required),
) -> StreamingResponse:
    """
    Chat with the AI-powered chatbot.

    **Note:**

    You need to sing up and sign in before calling this API. If you are using
    the Swagger UI. You can get the token automatically by login in through `api/auth/verify` API.

    **Anonymous users**, we will create anonymous usef infor in the database. So, you can login through Authorize button in Swagger UI.
    - **username**: anonymous
    - **password**: Marlboro@2211

    **Example of the request body:**

    ```bash
    curl -X 'POST'
    'http://localhost:8000/api/chat'
    -H 'accept: application/json'
    -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFub255bW91cyIsImVtYWlsIjoiYW5vbnltb3VzQGFub255LmNvbSIsImV4cCI6MTcyMTA3MTI0MCwic3ViIjoiWU9VUi1KV1QtU1VCSkVDVCJ9.hip3zPA2yN-MOwKHFOm_KhZuvaC4soY4MgwegyYJu2s'
    -H 'Content-Type: application/json'
    -d '{
    "sessionUuid": "string",
    "message": "do you know RMIT?",
    "temperature": 0.2,
    "topK": 40,
    "topP": 0.9,
    "nPredict": 512
    }'
    ```

    **Return StreamingResponse:**
    data: {"content":" Yes","stop":false,"id_slot":0,"multimodal":false}

    data: {"content":",","stop":false,"id_slot":0,"multimodal":false}

    data: {"content":" R","stop":false,"id_slot":0,"multimodal":false}

    data: {"content":"MIT","stop":false,"id_slot":0,"multimodal":false}

    data: {"content":" University","stop":false,"id_slot":0,"multimodal":false}

    """

    ##############################################################################################################################
    # Note: await keyword will cause issue. See https://github.com/sqlalchemy/sqlalchemy/discussions/9757
    #

    current_user = await account_repo.read_account_by_username(username=jwt_payload.username)

    # TODO: Only read session here @Micost
    session = await session_repo.read_create_sessions_by_uuid(
        session_uuid=chat_in_msg.sessionUuid, account_id=current_user.id, name=chat_in_msg.message[:20]
    )

    match session.type:
        case "rag":
            stream_func: ContentStream = rag_chat_repo.inference_with_rag(
                session_id=session.id,
                input_msg=chat_in_msg.message,
                temperature=chat_in_msg.temperature,
                top_k=chat_in_msg.top_k,
                top_p=chat_in_msg.top_p,
                n_predict=chat_in_msg.n_predict,
            )
        case _:  # default is chat robot
            stream_func: ContentStream = rag_chat_repo.inference_with_rag(
                session_id=session.id,
                input_msg=chat_in_msg.message,
                temperature=chat_in_msg.temperature,
                top_k=chat_in_msg.top_k,
                top_p=chat_in_msg.top_p,
                n_predict=chat_in_msg.n_predict,
            )

    # Buffering (the real problem) https://serverfault.com/questions/801628/for-server-sent-events-sse-what-nginx-proxy-configuration-is-appropriate/801629#
    return StreamingResponse(
        stream_func, headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}, media_type="text/event-stream"
    )


@router.get(
    path="",
    name="chat:get-session-of-current-user",
    response_model=list[Session],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_session(
    token: str = fastapi.Depends(oauth2_scheme),
    session_repo: SessionCRUDRepository = fastapi.Depends(get_repository(repo_type=SessionCRUDRepository)),
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
    jwt_payload: dict = fastapi.Depends(jwt_required),
) -> list[Session]:
    sessions_list: list = list()
    # Anonymous user won't related to any session
    if jwt_payload.username == ANONYMOUS_USER:
        return sessions_list
    current_user = await account_repo.read_account_by_username(username=jwt_payload.username)
    sessions = await session_repo.read_sessions_by_account_id(id=current_user.id)
    for session in sessions:
        loguru.logger.info(f"Session Details --- {session.name}")
        try:
            res_session = Session(
                sessionUuid=session.uuid,
                name=session.name,
                type=session.type,
                created_at=session.created_at,
            )
            sessions_list.append(res_session)
        except Exception as e:
            loguru.logger.info(f"Exception --- {e}")

    return sessions_list


@router.get(
    path="/history/{uuid}",
    name="chat:get-chat-history-by-session-uuid",
    response_model=list[ChatsWithTime],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_chathistory(
    uuid: str,
    token: str = fastapi.Depends(oauth2_scheme),
    chat_repo: ChatHistoryCRUDRepository = fastapi.Depends(get_repository(repo_type=ChatHistoryCRUDRepository)),
    session_repo: SessionCRUDRepository = fastapi.Depends(get_repository(repo_type=SessionCRUDRepository)),
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
    jwt_payload: dict = fastapi.Depends(jwt_required),
) -> list[ChatsWithTime]:
    """

    Get chat history to session by session uuid
    
    **Note:**
    Will verify if the user has access to the session
    Upper limit of the chat history is 50
    
    **Example of the request body:**

    ```bash
    curl -X 'GET' \
    'http://127.0.0.1:8000/api/chat/history/6dcf3f30-4521-4d8e-b944-e7e1b80c4861' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFub255bW91cyIsImVtYWlsIjoiYW5vbnltb3VzQGFub255LmNvbSIsImV4cCI6MTcyMTIxMjA3NCwic3ViIjoiWU9VUi1KV1QtU1VCSkVDVCJ9.WjKiLd5wLDlzV_T2UHx8i8WFwG-rXBWmCvhovb_9lC0'
    ```
    
    **Returns**
    ```json
    [
    {
        "role": "user",
        "message": "hello 1",
        "createAt": "2024-07-12T14:01:22.368636Z"
    },
    {
        "role": "assistant",
        "message": "hello 2",
        "createAt": "2024-07-12T14:01:22.368636Z"
    },
    {
        "role": "user",
        "message": "hello 3",
        "createAt": "2024-07-12T14:01:31.639983Z"
    },
    {
        "role": "assistant",
        "message": "hello 4",
        "createAt": "2024-07-12T14:01:31.639983Z"
    }
    ]
    ```
    """
    current_user = await account_repo.read_account_by_username(username=jwt_payload.username)
    if await session_repo.verify_session_by_account_id(session_uuid=uuid, account_id=current_user.id) is False:
        raise http_404_exc_uuid_not_found_request(uuid=uuid)
    session = await session_repo.read_sessions_by_uuid(session_uuid=uuid)
    chats = await chat_repo.read_chat_history_by_session_id(id=session.id)
    chats_list: list = list()
    for chat in chats:
        res_session = ChatsWithTime(
            role=chat.role,
            message=chat.message,
            create_at=chat.created_at,
        )
        chats_list.append(res_session)

    return chats_list


@router.post(
    path="/save",
    name="chat:save-chat-history-to-session",
    response_model=ChatUUIDResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def save_chats(
    chat_in_msg: SaveChatHistory,
    token: str = fastapi.Depends(oauth2_scheme),
    session_repo: SessionCRUDRepository = fastapi.Depends(get_repository(repo_type=SessionCRUDRepository)),
    chat_repo: ChatHistoryCRUDRepository = fastapi.Depends(get_repository(repo_type=ChatHistoryCRUDRepository)),
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
    jwt_payload: dict = fastapi.Depends(jwt_required),
) -> ChatUUIDResponse:
    """

    Save chat history to session by session uuid
    
    **Note:**
    
    No overlap chat histories
    Messages longer than 4096 characters will be truncated
        
    **Example of the request body:**

    ```bash
    curl -X 'POST' \
    'http://127.0.0.1:8000/api/chat/save' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFub255bW91cyIsImVtYWlsIjoiYW5vbnltb3VzQGFub255LmNvbSIsImV4cCI6MTcyMTIxMjA3NCwic3ViIjoiWU9VUi1KV1QtU1VCSkVDVCJ9.WjKiLd5wLDlzV_T2UHx8i8WFwG-rXBWmCvhovb_9lC0' \
    -H 'Content-Type: application/json' \
    -d '{
    "sessionUuid": "6dcf3f30-4521-4d8e-b944-e7e1b80c4861",
    "chats": [
        {
        "role": "user",
        "message": "hello"
        },
        {
        "role": "assistant",
        "message": "hi there, how can i help you?"
        },
        {
        "role": "user",
        "message": "I'\''m a billionaire but could not find a way to be happy."
        },
        {
        "role": "assistant",
        "message": "come on, time to wake up."
        }
    ]
    }'
    ```
    
    **Returns**

    {"sessionUuid": "6dcf3f30-4521-4d8e-b944-e7e1b80c4861"}

    """
    current_user = await account_repo.read_account_by_username(username=jwt_payload.username)
    if (
        session_repo.verify_session_by_account_id(session_uuid=chat_in_msg.sessionUuid, account_id=current_user.id)
        is False
    ):
        raise http_404_exc_uuid_not_found_request(uuid=chat_in_msg.sessionUuid)
    session = await session_repo.read_sessions_by_uuid(session_uuid=chat_in_msg.sessionUuid)
    await chat_repo.load_create_chat_history(session_id=session.id, chats=chat_in_msg.chats)
    return ChatUUIDResponse(sessionUuid=chat_in_msg.sessionUuid)
