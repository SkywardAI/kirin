import csv

from pymilvus import db

from src.config.settings.const import CHAT_COMTEXT, DEFAULT_MODEL, MAX_SQL_LENGTH, UPLOAD_FILE_PATH
from src.repository.rag.base import BaseRAGRepository
from src.repository.vector_database import vector_db

from . import encoder, model_pipeline, tokenizer


class RAGChatModelRepository(BaseRAGRepository):

    # nlp = pipeline("question-answering", model=model_name, tokenizer=model_name)

    async def load_model(self, session_id: int, model_name: str) -> bool:
        # Init model with input model_name
        try:
            # https://github.com/UKPLab/sentence-transformers/blob/85810ead37d02ef706da39e4a1757702d1b9f7c5/sentence_transformers/SentenceTransformer.py#L47
            # model = SentenceTransformer(model_name, device=get_device())
            # model.max_seq_length = MAX_SQL_LENGTH
            pass
        except Exception as e:
            print(e)
            return False
        return True

    def get_prompt(self, session_id: int, message: str, context: str) -> str:
        system_prompt = """"""
        # TODO get chat_history by session_id
        chat_history: list[tuple[str, str]] = []
        texts = [f"<s>[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n"]

        do_strip = False
        for user_input, response in chat_history:
            user_input = user_input.strip() if do_strip else user_input
            do_strip = True
            texts.append(f"{user_input} [/INST] {response.strip()} </s><s>[INST] ")
        message = message.strip() if do_strip else message

        texts.append(f"{message} [/INST]")

        return "".join(texts)

    def search_context(self, query, n_results=1):
        query_embeddings = encoder.encode(query).tolist()
        return vector_db.client.collection.query(query_embeddings=query_embeddings, n_results=n_results)

    async def get_response(self, session_id: int, input_msg: str) -> str:
        # TODO use RAG framework to generate the response message @Aisuko
        context = self.search_context(input_msg)
        prompt = self.get_prompt(session_id, input_msg, context)
        sequences = model_pipeline(
            prompt,
            max_length=500,
            do_sample=True,
            top_k=10,
            num_return_sequences=1,
            eos_token_id=tokenizer.eos_token_id,
        )
        # TODO stream output
        return "answer"

    async def load_csv_file(self, file_name: str, model_name: str) -> bool:
        # read file named file_name and convert the content into a list of strings @Aisuko
        print(file_name)
        print(model_name)
        data = []
        # self.embeddings = []
        # Open the CSV file
        with open(UPLOAD_FILE_PATH + file_name, "r") as file:
            # Create a CSV reader
            reader = csv.reader(file)

            # Iterate over each row in the CSV
            for row in reader:
                # Add the row to the list
                data.extend(row)
        for i, item in enumerate(data):
            embeddings = encoder.encode(item).tolist()
            print(i)
            res = vector_db.client.insert(collection_name="quick_setup", data={"id": i, "vector": embeddings})

        return res.success
