from src.models.schemas.base import BaseSchemaModel
from pydantic import(Field)

class ServiceVersionResponse(BaseSchemaModel):
    llamacpp_version: str | None = Field(..., title="llamacpp version", description="llamacpp version", examples=['gpt2-minimal-Q4_K_M-v2.gguf']) 
    milvus_version : str | None = Field(..., title="milvus version", description="milvus version", examples=['v2.3.12']) 
    backend_version :str | None = Field(..., title="backend service version", description="backend service version", examples=['v0.1.8']) 

