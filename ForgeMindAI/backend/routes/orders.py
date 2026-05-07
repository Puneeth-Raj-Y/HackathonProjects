import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from models.models import Order
from models.schemas import OrderSchema, QualityNoteRequest, StatusUpdateRequest
from services.order_service import add_order_note, get_order_by_id, list_orders, order_to_dict, update_order_status

logger = logging.getLogger("forgemind.orders")
router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.get("", response_model=list[OrderSchema])
def get_orders(user_id: int | None = None, status: str | None = None, db: Session = Depends(get_db)):
    logger.info("GET /api/orders user_id=%s status=%s", user_id, status)
    orders = list_orders(db, user_id=user_id, status=status)
    return orders


@router.get("/{order_id}", response_model=OrderSchema)
def get_order(order_id: int, db: Session = Depends(get_db)):
    logger.info("GET /api/orders/%s", order_id)
    order = get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.patch("/{order_id}/status", response_model=OrderSchema)
def patch_order_status(order_id: int, payload: StatusUpdateRequest, db: Session = Depends(get_db)):
    logger.info("PATCH /api/orders/%s/status -> %s", order_id, payload.status)
    order = get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return update_order_status(db, order, payload.status)


@router.post("/{order_id}/quality", response_model=OrderSchema)
def post_quality_note(order_id: int, payload: QualityNoteRequest, db: Session = Depends(get_db)):
    logger.info("POST /api/orders/%s/quality", order_id)
    order = get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return add_order_note(db, order, payload.note)
