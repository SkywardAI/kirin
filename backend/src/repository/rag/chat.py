import csv
import loguru

from src.models.schemas.train import TrainFileIn
import sqlalchemy
import loguru
from src.models.schemas.chat import MessagesResponse
from pymilvus import db
from datasets import load_dataset

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
        loguru.logger.info(f'ai generate_answer value:{answer}')
        # TODO stream output
        return answer

    async def load_csv_file(self, file_name: str, model_name: str) -> bool:
        # read file named file_name and convert the content into a list of strings @Aisuko
        loguru.logger.info(file_name)
        loguru.logger.info(model_name)
        data = []
        with open(UPLOAD_FILE_PATH + file_name, "r") as file:
            # Create a CSV reader
            reader = csv.reader(file)
            # Iterate over each row in the CSV
            for row in reader:
                # Add the row to the list
                data.extend(row)
        loguru.logger.info(f"load_csv_file data_row:{data}")                
        embedding_list = ai_model.encode_string(data)
        vector_db.insert_list(embedding_list, data)

        return True


    async def load_data_set(self, param: TrainFileIn)-> bool:

        if param.embedField is None or param.resField is None:
           loguru.logger.info(f"load_data_set param {param}")           
           await self.load_data_set_all_field(dataset_name=param.dataSet) 
        else:
           await self.load_data_set_by_field(param=param)   
        return True



    async def load_data_set_all_field(self, dataset_name: str)-> bool:
        loguru.logger.info(f"load_data_set_all_field dataset_name:{dataset_name}")
        reader_dataset=load_dataset(dataset_name)
        for item_dict in reader_dataset['train']:
            loguru.logger.info(f"load_data_set_all_field item_dict:{item_dict.get('url', '')},{type(item_dict)}")
            for key, value in item_dict.items():
                if(isinstance(key, str)):
                  embedding_list = ai_model.encode_string(value)
                  vector_db.insert_list(embedding_list, value)  
        return True



    async def load_data_set_by_field(self, param: TrainFileIn)->bool:
        reader_dataset=load_dataset(param.dataSet)
        embedField=param.embedField
        resField=  param.resField
        for item in reader_dataset['train']:
         # check contail field
            # if resField not in item or embedField not in item :
          embedField_val=item.get(embedField, '')
          resField_val=item.get(resField, '')
          embedding_list = ai_model.encode_string(embedField_val)         
          vector_db.insert_list(embedding_list, resField_val)  
            
        return True
