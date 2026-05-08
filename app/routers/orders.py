from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.database import get_db
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderStatusUpdate, OrderResponse
from app.middleware.auth import require_admin
from app.utils.errors import error_response

router = APIRouter(prefix="/api/orders", tags=["orders"])

@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(data: OrderCreate, db: Session = Depends(get_db)):
    order = Order(
        customer_name=data.customer_name,
        customer_email=data.customer_email,
        customer_phone=data.customer_phone,
        shipping_address=data.shipping_address.model_dump(),
        items=[item.model_dump() for item in data.items],
        total_ghs=data.total_ghs,
        total_usd=data.total_usd,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

@router.get("", response_model=List[OrderResponse], dependencies=[Depends(require_admin)])
def list_orders(status: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(Order).order_by(Order.created_at.desc())
    if status:
        q = q.filter(Order.status == status)
    return q.all()

@router.get("/{order_id}", response_model=OrderResponse, dependencies=[Depends(require_admin)])
def get_order(order_id: UUID, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", "Order not found"))
    return order

@router.patch("/{order_id}/status", response_model=OrderResponse, dependencies=[Depends(require_admin)])
def update_order_status(order_id: UUID, data: OrderStatusUpdate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", "Order not found"))
    order.status = data.status
    if data.payment_status:
        order.payment_status = data.payment_status
    db.commit()
    db.refresh(order)
    return order
