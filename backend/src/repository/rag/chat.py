from sentence_transformers import SentenceTransformer

from src.config.settings.const import DEFAULT_MODEL, MAX_SQL_LENGTH
from src.repository.rag.base import BaseRAGRepository


class RAGChatModelRepository(BaseRAGRepository):
    model = SentenceTransformer(DEFAULT_MODEL, "cuda")

    async def load_model(self, session_id: int, model_name: str) -> bool:
        # Init model with input model_name
        try:
            model = SentenceTransformer(model_name, "cuda")
            model.max_seq_length = MAX_SQL_LENGTH
        except Exception as e:
            print(e)
            return False
        return True

    async def get_response(self, session_id: int, input_msg: str) -> str:
        # TODO use RAG framework to generate the response message
        response_msg = "Oh, really? It's amazing !"
        return response_msg
