from pymilvus import connections

from src.config.manager import settings


class VectorDatabase:
    def __init__(self):
        try:
            connections.connect("default", host=settings.MILVUS_HOST, port=settings.MILVUS_PORT)
            print("Connected to Milvus.")
        except Exception as e:
            print(f"Failed to connect to Milvus: {e}")
            raise


vector_db: VectorDatabase = VectorDatabase()
