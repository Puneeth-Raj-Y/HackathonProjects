import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from models.schemas import DashboardSummary
from services.analytics_service import get_dashboard_summary, get_overview_orders

logger = logging.getLogger("forgemind.dashboard")
router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/overview", response_model=DashboardSummary)
def get_dashboard_overview(user_id: int = 1, role: str = "customer", db: Session = Depends(get_db)):
    logger.info("GET /api/dashboard/overview user_id=%s role=%s", user_id, role)
    return get_dashboard_summary(db, user_id=user_id, role=role)


@router.get("/orders")
def get_dashboard_orders(user_id: int = 1, role: str = "customer", db: Session = Depends(get_db)):
    logger.info("GET /api/dashboard/orders user_id=%s role=%s", user_id, role)
    return {"orders": get_overview_orders(db, user_id=user_id, role=role)}
