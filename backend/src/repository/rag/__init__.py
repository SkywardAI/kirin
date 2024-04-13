from src.config.settings.const import SAMPLE_CONTEXT
from src.repository.ai_models import ai_model
from datasets import load_dataset
from src.repository.vector_database import vector_db

# init vectorDB create the default collection
vector_db.create_collection()
# Create sample embeddings for testing
embedding_list=load_dataset('aisuko/sentences_of_Melbourne')
ps=embedding_list['train'].to_pandas().to_numpy()
vector_db.insert_list(ps, SAMPLE_CONTEXT)
print("Sample inserted")
