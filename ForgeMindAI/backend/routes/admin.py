import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from models.schemas import DashboardSummary, OrderSchema, QualityNoteRequest, StatusUpdateRequest
from services.analytics_service import get_dashboard_summary, get_overview_orders
from services.order_service import add_order_note, get_order_by_id, update_order_status

logger = logging.getLogger("forgemind.admin")
router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/overview", response_model=DashboardSummary)
def get_admin_overview(db: Session = Depends(get_db)):
    logger.info("GET /api/admin/overview")
    return get_dashboard_summary(db, role="admin")


@router.get("/orders")
def get_admin_orders(db: Session = Depends(get_db)):
    logger.info("GET /api/admin/orders")
    return {"orders": get_overview_orders(db, role="admin")}


@router.patch("/orders/{order_id}/status", response_model=OrderSchema)
def admin_patch_order_status(order_id: int, payload: StatusUpdateRequest, db: Session = Depends(get_db)):
    logger.info("PATCH /api/admin/orders/%s/status -> %s", order_id, payload.status)
    order = get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return update_order_status(db, order, payload.status)


@router.post("/orders/{order_id}/quality", response_model=OrderSchema)
def admin_post_order_note(order_id: int, payload: QualityNoteRequest, db: Session = Depends(get_db)):
    logger.info("POST /api/admin/orders/%s/quality", order_id)
    order = get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return add_order_note(db, order, payload.note)
