import time

from pymilvus import connections, Milvus, MilvusClient

from src.config.manager import settings
from src.config.settings.const import DEFAULT_COLLECTION, DEFAULT_DIM


class MilvusHelper:
    def __init__(self):
        for _ in range(3):
            try:
                url = f"http://{settings.MILVUS_HOST}:{settings.MILVUS_PORT}"
                self.client = MilvusClient(url)
                print("Connected to Milvus.")
                break
            except Exception as e:
                err = e
                # print(f"Failed to connect to Milvus: {e}")
                time.sleep(10)
        else:
            raise Exception(f"Failed to connect to Milvus after 3 attempts:{err}")

    def create_collection(self, collection_name=DEFAULT_COLLECTION, dimension=DEFAULT_DIM, recreate=True):
        if recreate and self.client.has_collection(collection_name):
            print(f"Milvus: collection {collection_name} exist, dropping..")
            self.client.drop_collection(collection_name)

        self.client.create_collection(collection_name=collection_name, dimension=dimension)
        print(f"Milvus: collection {collection_name} created")

    def insert_single(self, data, collection_name=DEFAULT_COLLECTION):
        try:
            dim = self._get_collection_dimension_(collection_name)
            if len(data) < dim:
                data += [0] * (dim - len(data))
            self.client.insert(collection_name, data)
        except Exception as e:
            print(f"Error: {e}")

    def insert_list(self, data, collection_name=DEFAULT_COLLECTION):
        try:
            dim = self._get_collection_dimension_(collection_name)
            for i, item in enumerate(data):
                if len(item) < dim:
                    item += [0] * (dim - len(item))
                self.client.insert(collection_name=collection_name, data={"id": i, "vector": item})
        except Exception as e:
            print(f"Error: {e}")

    def search(self, data, n_results, collection_name=DEFAULT_COLLECTION):
        dim = self._get_collection_dimension_(collection_name)
        if len(data) < dim:
            data += [0] * (dim - len(data))
        search_params = {"metric_type": "COSINE", "params": {}}

        # Search with limit
        res = self.client.search(
            collection_name=collection_name, data=data, limit=n_results, search_params=search_params
        )
        return res

    def create_index(self, index_name, index_params, collection_name=DEFAULT_COLLECTION):
        self.client.create_index(collection_name, index_name, index_params)

    def _get_collection_dimension_(self, collection_name=DEFAULT_COLLECTION):
        collection_info = self.client.get_collection_info(collection_name)
        return collection_info.dimension

    def __del__(self):
        self.client.close()


vector_db: MilvusHelper = MilvusHelper()
