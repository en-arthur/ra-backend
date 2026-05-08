from sqlalchemy import Column, String, Boolean, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy import DateTime
import uuid
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slug = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    price_ghs = Column(Numeric(10, 2), nullable=False)
    price_usd = Column(Numeric(10, 2), nullable=False)
    collection = Column(String)
    colors = Column(JSONB, default=list)
    color_hex = Column(JSONB, default=list)
    description = Column(Text)
    care = Column(JSONB, default=list)
    sizes = Column(JSONB, default=list)
    sold_out = Column(JSONB, default=list)
    images = Column(JSONB, default=list)
    category = Column(String)
    featured = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
