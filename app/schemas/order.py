from pydantic import BaseModel, EmailStr
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class ShippingAddress(BaseModel):
    line1: str
    line2: Optional[str] = None
    city: str
    region: str
    country: str = "Ghana"

class OrderItem(BaseModel):
    product_id: str
    slug: str
    name: str
    size: str
    color: str
    quantity: int
    price_ghs: float
    price_usd: float

class OrderCreate(BaseModel):
    customer_name: str
    customer_email: EmailStr
    customer_phone: Optional[str] = None
    shipping_address: ShippingAddress
    items: List[OrderItem]
    total_ghs: float
    total_usd: float

class OrderStatusUpdate(BaseModel):
    status: str
    payment_status: Optional[str] = None

class OrderResponse(BaseModel):
    id: UUID
    customer_name: str
    customer_email: str
    customer_phone: Optional[str]
    shipping_address: dict
    items: list
    total_ghs: Optional[float]
    total_usd: Optional[float]
    status: str
    payment_status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
