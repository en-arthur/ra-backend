from sqlalchemy import Column, String, Numeric, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy import DateTime
import uuid
from app.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_name = Column(String, nullable=False)
    customer_email = Column(String, nullable=False)
    customer_phone = Column(String)
    shipping_address = Column(JSONB, nullable=False)
    items = Column(JSONB, nullable=False)
    total_ghs = Column(Numeric(10, 2))
    total_usd = Column(Numeric(10, 2))
    status = Column(String, default="pending")
    payment_status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("status IN ('pending','processing','shipped','delivered','cancelled')", name="chk_order_status"),
        CheckConstraint("payment_status IN ('pending','paid','failed')", name="chk_payment_status"),
    )
