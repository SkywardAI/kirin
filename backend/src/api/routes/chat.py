import fastapi
import loguru

from src.api.dependencies.repository import get_rag_repository, get_repository
from src.securities.authorizations.jwt import jwt_required
from src.config.settings.const import ANONYMOUS_USER
from src.models.schemas.chat import ChatHistory, ChatInMessage, ChatInResponse, Session
from src.repository.crud.chat import ChatHistoryCRUDRepository, SessionCRUDRepository
from src.repository.crud.account import AccountCRUDRepository
from src.repository.rag.chat import RAGChatModelRepository

router = fastapi.APIRouter(prefix="/chat", tags=["chatbot"])


@router.post(
    "",
    name="chat:chatbot",
    response_model=ChatInResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def chat(
    chat_in_msg: ChatInMessage,
    session_repo: SessionCRUDRepository = fastapi.Depends(get_repository(repo_type=SessionCRUDRepository)),
    chat_repo: ChatHistoryCRUDRepository = fastapi.Depends(get_repository(repo_type=ChatHistoryCRUDRepository)),
    rag_chat_repo: RAGChatModelRepository = fastapi.Depends(get_rag_repository(repo_type=RAGChatModelRepository)),
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
    jwt_payload: dict = fastapi.Depends(jwt_required)
) -> ChatInResponse:
    # if not chat_in_msg.accountID:
    #     chat_in_msg.accountID = 0
    current_user = await account_repo.read_account_by_username(username=jwt_payload.username)
    if not hasattr(chat_in_msg, "sessionUuid") or not chat_in_msg.sessionUuid:
        new_session = await session_repo.create_session(
            account_id=current_user.id, name=chat_in_msg.message[:20]
        )
        session_uuid = new_session.uuid
    else:
        # TODO need verify if sesson exist
        # create_session = await session_repo.read_create_sessions_by_id(id=chat_in_msg.sessionId, account_id=chat_in_msg.accountID, name=chat_in_msg.message[:20])
        session_uuid = chat_in_msg.session_uuid
    # response_msg = await rag_chat_repo.get_response(session_id=session_id, input_msg=chat_in_msg.message, chat_repo=chat_repo)
    session = await session_repo.read_create_sessions_by_uuid(uuid=session_uuid,account_id=current_user.id, name=chat_in_msg.message[:20] )
    session_uuid = session.uuid
    response_msg=await rag_chat_repo.inference(session_id=session.id, input_msg=chat_in_msg.message, chat_repo=chat_repo)

    # score = await rag_chat_repo.evaluate_response(request_msg = chat_in_msg.message, response_msg = response_msg)
    # response_msg = response_msg + "score : {:.3f}".format(score)
    return ChatInResponse(
        sessionUuid=session_uuid,
        message=response_msg
    )


@router.get(
    path="",
    name="chat:get-session-of-current-user",
    response_model=list[Session],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_session(
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
