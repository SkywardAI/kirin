from datasets import load_dataset
from pymilvus import connections, DataType, db, MilvusClient
from sentence_transformers import SentenceTransformer

from src.repository.vector_database import vector_db

dataset = load_dataset("databricks/databricks-dolly-15k", split="train[:5]")
print(dataset)

closed_qa_dataset = dataset.filter(lambda example: example["category"] == "closed_qa")
print(closed_qa_dataset[0])
encoder = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1", device="cuda")
# Note: Fiting this according to the real word case

encoder.max_seq_length = 200
if vector_db.client.has_collection("quick_setup"):
    vector_db.client.drop_collection("quick_setup")

vector_db.client.create_collection(collection_name="quick_setup", dimension=384)
# res = vector_db.client.get_load_state(
#     collection_name="quick_setup"
# )

for i, item in enumerate(closed_qa_dataset):
    # each dataset entry, we generate and store an embedding of the combined 'instruction' and 'context' fields
    # with the context acting as the document for retrieval in our LLM prompts
    combined_text = f"{item['instruction']}, {item['context']}"
    embeddings = encoder.encode(combined_text).tolist()
    print(i)
    res = vector_db.client.insert(collection_name="quick_setup", data={"id": i, "vector": embeddings})
    # db.collection.add(embeddings=[embeddings], documents=[item['context']], ids=[f"id_{i}"])
    # self.collection.add(embeddings=[embeddings], documents=[item['context']],ids=[f"id_{i}"])
