import torch
from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, pipeline

from src.repository.vector_database import vector_db

# init vectorDB create the default collection
vector_db.create_collection()

# TODO init tokenizer
# TODO init model with default model @Aisuko
model_name = "deepset/roberta-base-squad2"
model_name = "tiiuae/falcon-7b-instruct"
dataset = load_dataset("databricks/databricks-dolly-15k", split="train[:5]")
print(dataset)

# closed_qa_dataset = dataset.filter(lambda example: example["category"] == "closed_qa")
# print(closed_qa_dataset[0])
encoder = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1", device="cuda")
# Note: Fiting this according to the real word case

encoder.max_seq_length = 200
tokenizer = AutoTokenizer.from_pretrained(model_name)
model_pipeline = pipeline(
    "text-generation",
    model=model_name,
    tokenizer=tokenizer,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    device_map="auto",
)
