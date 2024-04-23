from kimchima.pkg import PipelinesFactory
import sqlalchemy
from src.models.db.chat import ChatHistory

class ConversationWithSession:
    # init the converation with session id
    # Load chat history from db if the chat history exists
    def __init__(self, session_id, async_session):
        self.async_session=async_session
        self.session_id=session_id
        self.conversation = PipelinesFactory.init_conversation()
        self.load()

    # Load conversation to chat history 
    async def load(self):
        stmt = (
            sqlalchemy.select(ChatHistory)
            .where(ChatHistory.session_id == self.session_id)
            .order_by(ChatHistory.created_at.desc())
            .limit(10)
        )
        query = await self.async_session.execute(statement=stmt)
        db_Historys=query.scalars().all()
        for chat in db_Historys:
            role="assistant" if chat.is_bot_msg else "user"
            self.conversation.add_message({"role": role, "content": chat.message})

    async def save(self):
        for con in self.conversation:
            is_bot_msg = (con.role == "assistant")
            chat=ChatHistory(session_id=self.session_id, is_bot_msg=is_bot_msg, message=con.content)
            await self.async_session.add(instance=chat)
        await self.async_session.commit()

    # save converstiona to session id
    async def __del__(self):
        self.save()
        pass

