import csv
import loguru

from src.models.schemas.chat import MessagesResponse
from pymilvus import db

from src.models.db.chat import ChatHistory
from src.config.settings.const import UPLOAD_FILE_PATH
from src.repository.ai_models import ai_model
from src.repository.rag.base import BaseRAGRepository
from src.repository.vector_database import vector_db
from src.repository.conversation import ConversationWithSession, conversations

class RAGChatModelRepository(BaseRAGRepository):
    async def load_model(self, session_id: int, model_name: str) -> bool:
        # Init model with input model_name
        try:
            ai_model.initialize_model(model_name)
            pass
        except Exception as e:
            loguru.logger.info(f"Exception --- {e}")
            return False
        return True

    def search_context(self, query, n_results=1):
        query_embeddings = ai_model.encode_string(query)
        loguru.logger.info(f"Embeddings Shape --- {query_embeddings.shape}")
        return vector_db.search(data=query_embeddings, n_results=n_results)

    async def get_response(self, session_id: int, input_msg: str, chat_repo) -> str:

        if session_id not in conversations:
            conversations[session_id] = ConversationWithSession(session_id, chat_repo)
            await conversations[session_id].load()
        con = conversations[session_id]
        con.conversation.add_message({"role": "user", "content": input_msg})
        context = self.search_context(input_msg)
        answer = ai_model.generate_answer(con,context)
        loguru.logger.info(f"AI generate_answer value --- {answer}")
        # TODO stream output
        return answer

    async def load_csv_file(self, file_name: str, model_name: str) -> bool:
        # read file named file_name and convert the content into a list of strings @Aisuko
        loguru.logger.info(f"CSV Loader --- File Name: {file_name}")
        loguru.logger.info(f"CSV Loader --- Model Name: {model_name}")
        data = []
        with open(UPLOAD_FILE_PATH + file_name, "r") as file:
            # Create a CSV reader
            reader = csv.reader(file)
            # Iterate over each row in the CSV
            for row in reader:
                # Add the row to the list
                data.extend(row)
        embedding_list = ai_model.encode_string(data)
        vector_db.insert_list(embedding_list, data)

        return True

    async def evaluate_response(self, request_msg: str, response_msg: str) -> float:
        # TODO evluate the response and request message

        return 0
