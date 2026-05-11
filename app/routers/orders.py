from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.database import get_db
from app.models.order import Order
from app.models.customer_order import CustomerOrder
from app.schemas.order import OrderCreate, OrderStatusUpdate, OrderResponse
from app.middleware.auth import require_admin
from app.utils.errors import error_response

router = APIRouter(prefix="/api/orders", tags=["orders"])


def normalize_phone(phone: str) -> str:
    """Normalize Ghana phone: +233241234567 or 0241234567 → 0241234567"""
    phone = phone.strip().replace(" ", "").replace("-", "")
    if phone.startswith("+233"):
        phone = "0" + phone[4:]
    elif phone.startswith("233") and len(phone) > 10:
        phone = "0" + phone[3:]
    return phone


@router.get("/unviewed/{phone}")
def get_unviewed_count(phone: str, db: Session = Depends(get_db)):
    normalized = normalize_phone(phone)
    count = db.query(CustomerOrder).filter(
        CustomerOrder.phone == normalized,
        CustomerOrder.viewed == False
    ).count()
    return {"count": count}


@router.patch("/viewed/{order_id}")
def mark_order_viewed(order_id: UUID, db: Session = Depends(get_db)):
    db.query(CustomerOrder).filter(CustomerOrder.order_id == order_id).update({"viewed": True})
    db.commit()
    return {"ok": True}


@router.post("/track", response_model=List[OrderResponse])
def track_orders(payload: dict, db: Session = Depends(get_db)):
    phone = normalize_phone(payload.get("phone", ""))
    if not phone:
        raise HTTPException(status_code=400, detail=error_response("MISSING_PHONE", "Phone number required"))
    orders = db.query(Order).filter(Order.customer_phone == phone).order_by(Order.created_at.desc()).all()
    return orders


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(data: OrderCreate, db: Session = Depends(get_db)):
    phone = normalize_phone(data.customer_phone) if data.customer_phone else None
    order = Order(
        customer_name=data.customer_name,
        customer_email=data.customer_email,
        customer_phone=phone,
        shipping_address=data.shipping_address.model_dump(),
        items=[item.model_dump() for item in data.items],
        total_ghs=data.total_ghs,
        total_usd=data.total_usd,
    )
    db.add(order)
    db.flush()

    if phone:
        db.add(CustomerOrder(phone=phone, order_id=order.id))

    db.commit()
    db.refresh(order)
    return order


@router.get("", response_model=List[OrderResponse], dependencies=[Depends(require_admin)])
def list_orders(status: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(Order).order_by(Order.created_at.desc())
    if status:
        q = q.filter(Order.status == status)
    return q.all()


@router.get("/confirmation/{order_id}", response_model=OrderResponse)
def get_order_confirmation(order_id: UUID, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", "Order not found"))
    return order


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
