from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.database import get_db
from app.models.inventory import Inventory
from app.schemas.inventory import InventoryUpdate, InventoryResponse
from app.middleware.auth import require_admin
from app.utils.errors import error_response

router = APIRouter(prefix="/api/inventory", tags=["inventory"])

@router.get("", response_model=List[InventoryResponse], dependencies=[Depends(require_admin)])
def list_inventory(product_id: UUID = None, db: Session = Depends(get_db)):
    q = db.query(Inventory)
    if product_id:
        q = q.filter(Inventory.product_id == product_id)
    return q.all()

@router.patch("/{inventory_id}", response_model=InventoryResponse, dependencies=[Depends(require_admin)])
def update_inventory(inventory_id: UUID, data: InventoryUpdate, db: Session = Depends(get_db)):
    item = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not item:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", "Inventory item not found"))
    item.quantity = data.quantity
    db.commit()
    db.refresh(item)
    return item
