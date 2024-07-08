import fastapi
import loguru
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import StreamingResponse
from src.api.dependencies.repository import get_rag_repository, get_repository
from src.securities.authorizations.jwt import jwt_required
from src.config.settings.const import ANONYMOUS_USER
from src.models.schemas.chat import (
    ChatHistory, 
    ChatInMessage, 
    ChatInResponse, 
    Session,
    ChatUUIDResponse
    )
from src.repository.crud.chat import (
    ChatHistoryCRUDRepository, 
    SessionCRUDRepository
    )
from src.repository.crud.account import AccountCRUDRepository
from src.repository.rag.chat import RAGChatModelRepository

router = fastapi.APIRouter(prefix="/chat", tags=["chatbot"])
# Automatically get the token from the request header for Swagger UI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/verify")


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
    jwt_payload: dict = fastapi.Depends(jwt_required)
)->ChatUUIDResponse:
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
    new_session = await session_repo.create_session(
            account_id=current_user.id, name='new session'
        )
    session_uuid = new_session.uuid

    return ChatUUIDResponse(
        sessionUuid=session_uuid
    )

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
    chat_repo: ChatHistoryCRUDRepository = fastapi.Depends(get_repository(repo_type=ChatHistoryCRUDRepository)),
    rag_chat_repo: RAGChatModelRepository = fastapi.Depends(get_rag_repository(repo_type=RAGChatModelRepository)),
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
    jwt_payload: dict = fastapi.Depends(jwt_required)
) -> ChatInResponse:
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
    'http://127.0.0.1:8000/api/chat'
    -H 'accept: application/json'
    -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFub255bW91cyIsImVtYWlsIjoiYW5vbnltb3VzQGFub255LmNvbSIsImV4cCI6MTcyMDkxOTY4Nywic3ViIjoiWU9VUi1KV1QtU1VCSkVDVCJ9.29zUJQvD5dkC9XIRvTfZTFJoO5HzZTgj1JjKOKedg2g'
    -H 'Content-Type: application/json'
    -d '{
    "sessionUuid": "string",
    "message": "how are you?"
    }'
    ```

    **Return ChatInResponse:**
    data: {"content":" I","stop":false,"id_slot":0,"multimodal":false}

    data: {"content":"'","stop":false,"id_slot":0,"multimodal":false}

    data: {"content":"m","stop":false,"id_slot":0,"multimodal":false}

    data: {"content":"",
    "id_slot":0,"stop":true,
    "model":"models/Phi-3-mini-4k-instruct-q4.gguf",
    "tokens_predicted":58,"tokens_evaluated":46,
    "generation_settings":{},
    }

    """


    ##############################################################################################################################
    # Note: await keyword will cause issue. See https://github.com/sqlalchemy/sqlalchemy/discussions/9757
    # 

    # if not chat_in_msg.accountID:
    #     chat_in_msg.accountID = 0
    current_user = await account_repo.read_account_by_username(username=jwt_payload.username)

    # TODO need verify if sesson exist
    # create_session = await session_repo.read_create_sessions_by_id(id=chat_in_msg.sessionId, account_id=chat_in_msg.accountID, name=chat_in_msg.message[:20])
    # response_msg = await rag_chat_repo.get_response(session_id=session_id, input_msg=chat_in_msg.message, chat_repo=chat_repo)

    # TODO: name=chat_in_msg.message[:20] can be edited
    session = await session_repo.read_create_sessions_by_uuid(session_uuid=chat_in_msg.sessionUuid, account_id=current_user.id, name=chat_in_msg.message[:20] )
    # response_msg=await rag_chat_repo.inference(session_id=session.id, input_msg=chat_in_msg.message, chat_repo=chat_repo)

    # score = await rag_chat_repo.evaluate_response(request_msg = chat_in_msg.message, response_msg = response_msg)
    # response_msg = response_msg + "score : {:.3f}".format(score)
    return StreamingResponse(
        rag_chat_repo.inference(session_id=session.id, input_msg=chat_in_msg.message, chat_repo=chat_repo), 
        media_type='text/event-stream'
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
    jwt_payload: dict = fastapi.Depends(jwt_required)
) -> list[Session]:
    sessions_list: list = list()
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
                created_at=session.created_at,
            )
            sessions_list.append(res_session)
        except Exception as e:
            loguru.logger.info(f"Exception --- {e}")

    return sessions_list

@router.get(
    path="/history/{uuid}",
    name="chat:get-chat-history-by-session-uuid",
    response_model=list[ChatHistory],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_chathistory(
    uuid: str,
    token: str = fastapi.Depends(oauth2_scheme),
    chat_repo: ChatHistoryCRUDRepository = fastapi.Depends(get_repository(repo_type=ChatHistoryCRUDRepository)),
    session_repo: SessionCRUDRepository = fastapi.Depends(get_repository(repo_type=SessionCRUDRepository)),
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
    jwt_payload: dict = fastapi.Depends(jwt_required)
) -> list[ChatHistory]:
    current_user = await account_repo.read_account_by_username(username=jwt_payload.username)
    if session_repo.verify_session_by_account_id(session_uuid=uuid, account_id=current_user.id) is False:
        raise fastapi.HTTPException(status_code=404, detail="Session not found")
    session = await session_repo.read_sessions_by_uuid(session_uuid=uuid)
    chats = await chat_repo.read_chat_history_by_session_id(id=session.id)
    chats_list: list = list()
    for chat in chats:
        res_session = ChatHistory(
            id=chat.id,
            type="out" if chat.is_bot_msg else "in",
            message=chat.message,
        )
        chats_list.append(res_session)

    return chats_list
