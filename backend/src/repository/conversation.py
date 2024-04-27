import time

from sqlalchemy.orm import Session
from src.repository.database import async_db
from datetime import datetime
from kimchima.pkg import PipelinesFactory
from src.models.db.chat import ChatHistory
from src.config.settings.const import CONVERSATION_INACTIVE_SEC

class ConversationWithSession:
    # init the converation with session id
    # Load chat history from db if the chat history exists
    def __init__(self, session_id, chat_repo):
        self.chat_repo=chat_repo
        self.session_id=session_id
        self.conversation = PipelinesFactory.init_conversation()
        self._last_used= datetime.now()
    
    def set_last_answer(self, answer):
        if len(self.conversation) > 50:
            self.conversation = self.conversation[-50:]
        self.conversation[-1]["content"] = answer
        self._last_used= datetime.now()

    def get_last_used(self):
        return self._last_used

    # Load conversation to chat history 
    async def load(self):
        db_Historys=await self.chat_repo.read_chat_history_by_session_id(id=self.session_id, limit_num=5)
        for chat in db_Historys:
            role="assistant" if chat.is_bot_msg else "user"
            self.conversation.add_message({"role": role, "content": chat.message})

    # save converstiona to session id
    def save(self):
        chat_list=[]
        session = Session(async_db.sync_engine)
        for con in self.conversation:
            is_bot_msg = (con["role"] == "assistant")
            chat=ChatHistory(session_id=self.session_id, is_bot_msg=is_bot_msg, message=con["content"])
            chat_list.append(chat)
            session.add(chat)
        session.commit()


    def __del__(self):
        pass

conversations = {}


def cleanup_conversations():
    while True:
        now = datetime.now()
        for session_id, conversation in list(conversations.items()):
            if (now - conversation.get_last_used()).total_seconds() > CONVERSATION_INACTIVE_SEC:
                conversation.save()
                del conversations[session_id]
        #check every 10s
        time.sleep(10)