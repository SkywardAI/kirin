import time
import loguru
import numpy as np
from pymilvus import MilvusClient
from src.config.manager import settings
from src.config.settings.const import DEFAULT_COLLECTION, DEFAULT_DIM


class MilvusHelper:
    def __init__(self):
        for _ in range(3):
            try:
                url = f"http://{settings.MILVUS_HOST}:{settings.MILVUS_PORT}"
                self.client = MilvusClient(url)
                loguru.logger.info("Vector Database --- Connected to Milvus.")
                break
            except Exception as e:
                err = e
                #loguru.logger.info(f"Exception --- {e}")
                # print(f"Failed to connect to Milvus: {e}")
                time.sleep(10)
        else:
            raise Exception(f"Failed to connect to Milvus after 3 attempts:{err}")

    async def load_dataset(self, *args, **kwargs):
        return
    
    async def load_csv(self, *args, **kwargs):
        return 
        
    async def save(self, *args, **kwargs):
        r"""
        Save data into vector database.

        Args:
        """

        return
    

    def create_collection(self, collection_name=DEFAULT_COLLECTION, dimension=DEFAULT_DIM, recreate=True):
        if recreate and self.client.has_collection(collection_name):
            loguru.logger.info(f"Vector Databse --- Milvus: collection {collection_name} exist, dropping..")
            self.client.drop_collection(collection_name)

        self.client.create_collection(collection_name=collection_name, dimension=dimension)
        loguru.logger.info(f"Vector Database --- Milvus: collection {collection_name} created")

    def insert_list(self, embedding, data, collection_name=DEFAULT_COLLECTION, start_idx=0):
        loguru.logger.info(f"Start insert data to {collection_name}")
        try:
            for i, item in enumerate(embedding):
                original_vector = np.array(item)
                padding_value = 0 
                if len(original_vector) > DEFAULT_DIM:
                    loguru.logger.info(f"Vector Databse --- Error: Vector dimension is larger than {DEFAULT_DIM}")
                    continue
                if len(original_vector) < DEFAULT_DIM:
                    padding_vector = np.ones(DEFAULT_DIM - len(original_vector)) * padding_value
                    padded_vector = np.concatenate((original_vector, padding_vector))
                else:
                    padded_vector = original_vector
                self.client.insert(collection_name=collection_name, data={"id": i+start_idx, "vector": padded_vector, "doc": data[i]})
        except Exception as e:
            loguru.logger.info(f"Vector Databse --- Error: {e}")
        loguru.logger.info("Complete insert!")

    def search(self, data, n_results, collection_name=DEFAULT_COLLECTION):

        search_params = {"metric_type": "COSINE", "params": {}}
        data_list = data.tolist()
        res = self.client.search(
            collection_name=collection_name,
            data=data_list,
            limit=n_results,
            search_params=search_params,
            output_fields=["doc"],
        )
        loguru.logger.info(f"Vector Database --- Result: {res}")
        sentences = []
        for hits in res:
            for hit in hits:
                sentences.append(hit.get("entity").get("doc"))
        return sentences

    def create_index(self, index_name, index_params, collection_name=DEFAULT_COLLECTION):
        self.client.create_index(collection_name, index_name, index_params)

    def _get_collection_dimension_(self, collection_name=DEFAULT_COLLECTION):
        # collection_info = self.client.get_collection(collection_name)
        # return collection_info.schema.dimension
        return DEFAULT_DIM

    def __del__(self):
        self.client.close()


vector_db: MilvusHelper = MilvusHelper()
