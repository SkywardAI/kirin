import csv

from src.config.settings.const import CHAT_COMTEXT, DEFAULT_MODEL, MAX_SQL_LENGTH, UPLOAD_FILE_PATH
from src.repository.rag.base import BaseRAGRepository
from src.utilities.devices.devices import get_device


class RAGChatModelRepository(BaseRAGRepository):

    async def load_model(self, session_id: int, model_name: str) -> bool:
        # Init model with input model_name
        try:
            pass
        except Exception as e:
            print(e)
            return False
        return True

    async def get_response(self, session_id: int, input_msg: str) -> str:
        # TODO use RAG framework to generate the response message @Aisuko
        # query_embedding = self.model.encode(input_msg, convert_to_tensor=True).to("cuda")
        # we use cosine-similarity and torch.topk to find the highest 5 scores
        # cos_scores = cos_sim(query_embedding, self.embeddings)[0]
        # top_results = torch.topk(cos_scores, k=1)
        # response_msg = self.data[top_results[1].item()]
        return "response message"

    async def load_csv_file(self, file_name: str, model_name: str) -> bool:
        # read file named file_name and convert the content into a list of strings @Aisuko
        print(file_name)
        print(model_name)
        self.data = []
        self.embeddings = []
        # Open the CSV file
        with open(UPLOAD_FILE_PATH + file_name, "r") as file:
            # Create a CSV reader
            reader = csv.reader(file)

            # Iterate over each row in the CSV
            for row in reader:
                # Add the row to the list
                self.data.extend(row)
        print(self.data)
        row_embedding = self.model.encode(self.data, convert_to_tensor=True).to("cuda")
        # TODO
        self.embeddings.append(row_embedding)
        return True
