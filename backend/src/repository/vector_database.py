import time
import loguru

from pymilvus import MilvusClient
from src.config.manager import settings
from src.config.settings.const import DEFAULT_COLLECTION, DEFAULT_DIM

import lancedb
import pandas as pd
import pyarrow as pa


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
                # loguru.logger.info(f"Exception --- {e}")
                # print(f"Failed to connect to Milvus: {e}")
                time.sleep(5)
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

        self.client.create_collection(
            collection_name=collection_name,
            dimension=dimension,
            auto_id=True,  # enable auto id
            enable_dynamic_field=True,  # enable dynamic field
            vector_field_name="question_embedding",  # map vector field name and embedding field name
            consistency_level="Strong",  # To enable search with latest data
        )
        loguru.logger.info(f"Vector Database --- Milvus: collection {collection_name} created")

    def insert_list(self, collection_name: str = DEFAULT_COLLECTION, data_list: list = []) -> dict:
        try:
            return self.client.insert(collection_name=collection_name, data=data_list)
        except Exception as e:
            loguru.logger.info(f"Vector Databse --- Error: {e}")

    def search(self, data, n_results, collection_name=DEFAULT_COLLECTION):
        search_params = {"metric_type": "COSINE", "params": {}}
        try:
            res = self.client.search(
                collection_name=collection_name,
                data=[data],
                limit=n_results,
                search_params=search_params,
                output_fields=["answer"],
            )

            loguru.logger.info(f"Vector Database --- Result: {res}")
            sentences = []
            for hits in res:
                for hit in hits:
                    sentences.append(hit.get("entity").get("answer"))
            return sentences
        except Exception as e:
            loguru.logger.error(e)
        return None

    def create_index(self, index_name, index_params, collection_name=DEFAULT_COLLECTION):
        self.client.create_index(collection_name, index_name, index_params)

    def _get_collection_dimension_(self, collection_name=DEFAULT_COLLECTION):
        # collection_info = self.client.get_collection(collection_name)
        # return collection_info.schema.dimension
        return DEFAULT_DIM

    def __del__(self):
        self.client.close()

class LanceHelper:
    def __init__(self):
        uri = "/vdata/default-lancedb"
        self.db = lancedb.connect(uri)

    def create_table(self, table_name=DEFAULT_COLLECTION, data: list =[], recreate=True):
        try:
            if recreate:
                self.db.create_table(table_name, data=data , mode="overwrite")
            else:
                self.db.create_table(table_name, data=data)
        except Exception as e:
            loguru.logger.error(e)
        return None
    
    def insert_list(self, table_name: str = DEFAULT_COLLECTION, data_list: list = []):
        try:
            tbl = self.db.open_table(table_name)
            tbl.add(data_list)
        except Exception as e:
            loguru.logger.info(f"Vector Databse --- Error: {e}")
    
    def search(self, data, n_results, table_name=DEFAULT_COLLECTION):
        print(table_name)
        try:
            tbl = self.db.open_table(table_name)
            df = tbl.search(data) \
                .limit(n_results) \
                .to_list()
            return df
        except Exception as e:
            loguru.logger.error(e)
        return None

# vector_db: MilvusHelper = MilvusHelper()
vector_db: MilvusHelper = LanceHelper()
