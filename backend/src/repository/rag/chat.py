import csv

import torch
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

from src.config.settings.const import CHAT_COMTEXT, DEFAULT_MODEL, MAX_SQL_LENGTH, UPLOAD_FILE_PATH
from src.repository.rag.base import BaseRAGRepository
from src.utilities.devices.devices import get_device


class RAGChatModelRepository(BaseRAGRepository):
    # TODO init model with default model @Aisuko
    model_name = "deepset/roberta-base-squad2"

    nlp = pipeline("question-answering", model=model_name, tokenizer=model_name)

    async def load_model(self, session_id: int, model_name: str) -> bool:
        # Init model with input model_name
        try:
            # https://github.com/UKPLab/sentence-transformers/blob/85810ead37d02ef706da39e4a1757702d1b9f7c5/sentence_transformers/SentenceTransformer.py#L47
            model = SentenceTransformer(model_name, device=get_device())
            model.max_seq_length = MAX_SQL_LENGTH
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
        QA_input = {"question": input_msg, "context": CHAT_COMTEXT}
        res = self.nlp(QA_input)
        return res["answer"]

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
        self.model = SentenceTransformer(model_name, "cuda")
        row_embedding = self.model.encode(self.data, convert_to_tensor=True).to("cuda")
        # TODO
        self.embeddings.append(row_embedding)
        return True
