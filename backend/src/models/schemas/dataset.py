
import datetime
from src.models.schemas.base import BaseSchemaModel


class DatasetCreate(BaseSchemaModel):
    dataset_name: str
    des: str | None = None

 

class DatasetResponse(BaseSchemaModel):
    id: int
    dataset_name: str  
    created_at: datetime.datetime | None=None       
    updated_at: datetime.datetime | None=None       