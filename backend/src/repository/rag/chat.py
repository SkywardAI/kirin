from src.repository.rag.base import BaseRAGRepository


class RAGChatModelRepository(BaseRAGRepository):
    async def get_response(self, session_id: int, input_msg: str) -> str:
        # TODO use RAG framework to generate the response message
        response_msg = "Oh, really? It's amazing !"
        return response_msg
