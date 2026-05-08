from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class InventoryUpdate(BaseModel):
    quantity: int

class InventoryResponse(BaseModel):
    id: UUID
    product_id: UUID
    size: str
    color: str
    quantity: int
    updated_at: datetime

    model_config = {"from_attributes": True}
