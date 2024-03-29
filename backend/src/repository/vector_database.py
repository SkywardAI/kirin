from pymilvus import connections, Milvus, MilvusClient

from src.config.manager import settings


class VectorDatabase:
    def __init__(self):
        try:
            url = f"http://{settings.MILVUS_HOST}:{settings.MILVUS_PORT}"
            self.client = MilvusClient(url)
            print("Connected to Milvus.")
        except Exception as e:
            print(f"Failed to connect to Milvus: {e}")
            raise


vector_db: VectorDatabase = VectorDatabase()
