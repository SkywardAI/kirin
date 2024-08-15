import loguru

from src.config.settings.const import DEFAULT_COLLECTION, META_LANCEDB

import lancedb

class MetaDBHelper:
    def __init__(self):
        self.db = lancedb.connect(META_LANCEDB)

        
meta_db: MetaDBHelper = MetaDBHelper()
