import loguru

from src.config.settings.const import DEFAULT_COLLECTION

import lancedb

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
                .select(["answer"]) \
                .to_list()
            return df[0].get("answer")
        except Exception as e:
            loguru.logger.error(e)
        return None

# vector_db: MilvusHelper = MilvusHelper()
vector_db: LanceHelper = LanceHelper()
