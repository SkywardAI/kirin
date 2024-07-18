
import datetime

from pydantic import Field
from src.models.schemas.base import BaseSchemaModel


class DatasetCreate(BaseSchemaModel):
    dataset_name: str = Field(..., title="DataSet Name", description="DataSet Name")
    des: str | None  = Field(..., title="Details", description="Details")
 
 

class DatasetResponse(BaseSchemaModel):
    id: int  = Field(..., title="id",description="id") 
    dataset_name: str = Field(..., title="DataSet Name", description="DataSet Name") 
    created_at: datetime.datetime | None  = Field(..., title="Creation time", description="Creation time")
    updated_at: datetime.datetime | None = Field(..., title="Update  time", description="Update time")   