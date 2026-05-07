from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from models.models import Order, User
from services.order_service import order_to_dict


def get_overview_orders(db: Session, user_id: Optional[int] = None, role: str = "customer") -> List[Dict[str, Any]]:
    query = db.query(Order)
    if role != "admin" and user_id is not None:
        query = query.filter(Order.user_id == user_id)
    orders = query.order_by(Order.created_at.desc()).all()
    return [order_to_dict(order) for order in orders]


def get_dashboard_summary(db: Session, user_id: Optional[int] = None, role: str = "customer") -> Dict[str, Any]:
    query = db.query(Order)
    if role != "admin" and user_id is not None:
        query = query.filter(Order.user_id == user_id)

    orders = query.all()
    total_orders = len(orders)
    pending = sum(1 for order in orders if order.status == "Pending")
    processing = sum(1 for order in orders if order.status == "Processing")
    completed = sum(1 for order in orders if order.status == "Completed")
    total_users = db.query(User).count()
    recent_orders = [order_to_dict(order) for order in sorted(orders, key=lambda item: item.created_at, reverse=True)[:6]]

    return {
        "total_orders": total_orders,
        "pending": pending,
        "processing": processing,
        "completed": completed,
        "total_users": total_users,
        "recent_orders": recent_orders,
    }
