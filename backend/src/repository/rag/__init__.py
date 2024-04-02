from src.config.settings.const import SAMPLE_CONTEXT
from src.repository.ai_models import ai_model
from src.repository.vector_database import vector_db

# init vectorDB create the default collection
vector_db.create_collection()
# create sample csv
embedding_list = ai_model.encode_string(SAMPLE_CONTEXT)
vector_db.insert_list(embedding_list)
