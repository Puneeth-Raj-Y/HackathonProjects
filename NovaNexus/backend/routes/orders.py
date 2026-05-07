from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database.db import get_db
from models import models, schemas
import logging

logger = logging.getLogger("forgemind.orders")

router = APIRouter(
    prefix="/api/orders",
    tags=["orders"]
)

# =========================
# ANALYTICS ROUTE FIRST
# =========================
@router.get("/analytics/summary")
def get_admin_stats(db: Session = Depends(get_db)):
    try:
        total_orders = db.query(models.Order).count()
        pending = db.query(models.Order).filter(models.Order.status == "Pending").count()
        processing = db.query(models.Order).filter(models.Order.status == "Processing").count()
        completed = db.query(models.Order).filter(models.Order.status == "Completed").count()
        total_users = db.query(models.User).count()

        return {
            "total_orders": total_orders,
            "pending": pending,
            "processing": processing,
            "completed": completed,
            "total_users": total_users
        }

    except Exception as e:
        logger.error(f"Analytics error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch analytics")


# =========================
# GET ALL ORDERS
# =========================
@router.get("/", response_model=List[schemas.OrderSchema])
def get_orders(
    user_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    try:
        query = db.query(models.Order)

        if user_id is not None:
            query = query.filter(models.Order.customer_id == user_id)

        if status:
            query = query.filter(models.Order.status == status)

        orders = query.all()

        return orders

    except Exception as e:
        logger.error(f"Get orders error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch orders")


# =========================
# GET SINGLE ORDER
# =========================
@router.get("/{order_id}", response_model=schemas.OrderSchema)
def get_order(order_id: int, db: Session = Depends(get_db)):
    try:
        order = db.query(models.Order).filter(models.Order.id == order_id).first()

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        return order

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Get order error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch order")


# =========================
# UPDATE STATUS
# =========================
@router.patch("/{order_id}/status")
def update_order_status(
    order_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    try:
        order = db.query(models.Order).filter(models.Order.id == order_id).first()

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        order.status = status
        db.commit()

        return {
            "message": "Status updated successfully",
            "order_id": order_id,
            "new_status": status
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Status update error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update status")


# =========================
# QUALITY LOG
# =========================
@router.post("/{order_id}/quality")
def add_quality_log(
    order_id: int,
    note: str,
    db: Session = Depends(get_db)
):
    try:
        order = db.query(models.Order).filter(models.Order.id == order_id).first()

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        new_log = models.QualityLog(
            order_id=order_id,
            note=note
        )

        db.add(new_log)
        db.commit()

        return {
            "message": "Quality log added successfully",
            "order_id": order_id
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Quality log error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to add quality log")
