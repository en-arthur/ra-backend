from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from uuid import UUID
import httpx
from app.database import get_db
from app.models.order import Order
from app.config import settings
from app.utils.errors import error_response

router = APIRouter(prefix="/api/paystack", tags=["paystack"])

PAYSTACK_BASE = "https://api.paystack.co"

def paystack_headers():
    return {"Authorization": f"Bearer {settings.paystack_secret_key}"}

class InitializeRequest(BaseModel):
    order_id: UUID
    email: str
    amount_ghs: float  # in GHS, we convert to pesewas

@router.post("/initialize")
async def initialize_payment(data: InitializeRequest, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == data.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", "Order not found"))

    amount_pesewas = int(data.amount_ghs * 100)

    async with httpx.AsyncClient() as client:
        res = await client.post(
            f"{PAYSTACK_BASE}/transaction/initialize",
            headers=paystack_headers(),
            json={
                "email": data.email,
                "amount": amount_pesewas,
                "currency": "GHS",
                "reference": str(data.order_id),
                "metadata": {"order_id": str(data.order_id)},
            },
        )

    if res.status_code != 200:
        raise HTTPException(status_code=502, detail=error_response("PAYSTACK_ERROR", "Failed to initialize payment"))

    result = res.json()
    return {
        "authorization_url": result["data"]["authorization_url"],
        "access_code": result["data"]["access_code"],
        "reference": result["data"]["reference"],
    }

@router.get("/verify/{reference}")
async def verify_payment(reference: str, db: Session = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{PAYSTACK_BASE}/transaction/verify/{reference}",
            headers=paystack_headers(),
        )

    if res.status_code != 200:
        raise HTTPException(status_code=502, detail=error_response("PAYSTACK_ERROR", "Failed to verify payment"))

    data = res.json()["data"]
    status = data["status"]

    if status == "success":
        # Update order payment status
        order = db.query(Order).filter(Order.id == reference).first()
        if order:
            order.payment_status = "paid"
            order.status = "processing"
            db.commit()

    return {"status": status, "reference": reference}
