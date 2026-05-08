from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class ProductBase(BaseModel):
    slug: str
    name: str
    price_ghs: float
    price_usd: float
    collection: Optional[str] = None
    colors: List[str] = []
    color_hex: List[str] = []
    description: Optional[str] = None
    care: List[str] = []
    sizes: List[str] = []
    sold_out: List[str] = []
    images: List[str] = []
    category: Optional[str] = None
    featured: bool = False

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price_ghs: Optional[float] = None
    price_usd: Optional[float] = None
    collection: Optional[str] = None
    colors: Optional[List[str]] = None
    color_hex: Optional[List[str]] = None
    description: Optional[str] = None
    care: Optional[List[str]] = None
    sizes: Optional[List[str]] = None
    sold_out: Optional[List[str]] = None
    images: Optional[List[str]] = None
    category: Optional[str] = None
    featured: Optional[bool] = None

class ProductResponse(ProductBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
