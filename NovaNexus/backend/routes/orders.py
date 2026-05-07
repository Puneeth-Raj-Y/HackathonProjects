from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.db import get_db
import logging

logger = logging.getLogger("forgemind.orders")

router = APIRouter(prefix="/api/orders", tags=["orders"])

@router.get("/", response_model=List[schemas.OrderSchema])
def get_orders(user_id: int = None, status: str = None, db: Session = Depends(get_db)):
    logger.info(f"REQUEST [GET ORDERS]: user_id={user_id}, status={status}")
    query = db.query(models.Order)
    if user_id:
        query = query.filter(models.Order.customer_id == user_id)
    if status:
        query = query.filter(models.Order.status == status)
    return query.all()

@router.get("/{order_id}", response_model=schemas.OrderSchema)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.patch("/{order_id}/status")
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = status
    db.commit()
    return {"message": "Status updated", "order_id": order_id, "new_status": status}

@router.post("/{order_id}/quality")
def add_quality_log(order_id: int, note: str, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    new_log = models.QualityLog(order_id=order_id, note=note)
    db.add(new_log)
    db.commit()
    return {"message": "Quality log added", "order_id": order_id}

@router.get("/analytics/summary")
def get_admin_stats(db: Session = Depends(get_db)):
    logger.info("REQUEST [GET STATS]: Fetching analytics summary")
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
