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
    if not hasattr(chat_in_msg, "sessionId") or not chat_in_msg.sessionId:
        new_session = await session_repo.create_session(
            account_id=current_user.id, name=chat_in_msg.message[:20]
        )
        session_id = new_session.id
    else:
        # TODO need verify if sesson exist
        # create_session = await session_repo.read_create_sessions_by_id(id=chat_in_msg.sessionId, account_id=chat_in_msg.accountID, name=chat_in_msg.message[:20])
        session_id = chat_in_msg.sessionId
    # response_msg = await rag_chat_repo.get_response(session_id=session_id, input_msg=chat_in_msg.message, chat_repo=chat_repo)

    response_msg=await rag_chat_repo.inference(session_id=session_id, input_msg=chat_in_msg.message, chat_repo=chat_repo)

    # score = await rag_chat_repo.evaluate_response(request_msg = chat_in_msg.message, response_msg = response_msg)
    # response_msg = response_msg + "score : {:.3f}".format(score)
    return ChatInResponse(
        sessionId=session_id,
        message=response_msg
    )


@router.get(
    path="/",
    name="chat:get-session-by-account-id",
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
                id=session.id,
                name=session.name,
                created_at=session.created_at,
            )
            sessions_list.append(res_session)
        except Exception as e:
            loguru.logger.info(f"Exception --- {e}")

    return sessions_list

@router.get(
    path="/history/{id}",
    name="chat:get-chat-history-by-session-id",
    response_model=list[ChatHistory],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_chathistory(
    id: int,
    chat_repo: ChatHistoryCRUDRepository = fastapi.Depends(get_repository(repo_type=ChatHistoryCRUDRepository)),
    session_repo: SessionCRUDRepository = fastapi.Depends(get_repository(repo_type=SessionCRUDRepository)),
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
    jwt_payload: dict = fastapi.Depends(jwt_required)
) -> list[ChatHistory]:
    current_user = await account_repo.read_account_by_username(username=jwt_payload.username)
    if session_repo.verify_session_by_account_id(session_id=id, account_id=current_user.id) is False:
        raise fastapi.HTTPException(status_code=404, detail="Session not found")
    chats = await chat_repo.read_chat_history_by_session_id(id=id)
    chats_list: list = list()
    for chat in chats:
        res_session = ChatHistory(
            id=chat.id,
            type="out" if chat.is_bot_msg else "in",
            message=chat.message,
        )
        chats_list.append(res_session)

    return chats_list
