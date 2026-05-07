import json
from collections import defaultdict
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from models.models import AnalyticsEvent, Order, OrderItem, User


DEFAULT_CUSTOMER = {
    "id": 1,
    "email": "customer@forgemind.ai",
    "role": "customer",
}

DEFAULT_ADMIN = {
    "id": 2,
    "email": "admin@forgemind.ai",
    "role": "admin",
}


def ensure_seed_data(db: Session) -> None:
    if db.get(User, 1) is None:
        db.add(User(**DEFAULT_CUSTOMER))
    if db.get(User, 2) is None:
        db.add(User(**DEFAULT_ADMIN))
    db.commit()


def order_to_dict(order: Order) -> Dict[str, Any]:
    return {
        "id": order.id,
        "user_id": order.user_id,
        "status": order.status,
        "deadline": order.deadline,
        "source_message": order.source_message,
        "created_at": order.created_at.isoformat() if order.created_at else None,
        "updated_at": order.updated_at.isoformat() if order.updated_at else None,
        "items": [
            {
                "id": item.id,
                "product_name": item.product_name,
                "category": item.category,
                "quantity": item.quantity,
                "specification": item.specification,
            }
            for item in order.items
        ],
    }


def list_orders(db: Session, user_id: Optional[int] = None, status: Optional[str] = None) -> List[Order]:
    query = db.query(Order)
    if user_id is not None:
        query = query.filter(Order.user_id == user_id)
    if status:
        query = query.filter(Order.status == status)
    return query.order_by(Order.created_at.desc()).all()


def get_order_by_id(db: Session, order_id: int) -> Optional[Order]:
    return db.query(Order).filter(Order.id == order_id).first()


def create_orders_from_items(
    db: Session,
    user_id: int,
    items: List[Dict[str, Any]],
    source_message: str,
) -> List[Order]:
    grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for item in items:
        grouped[item.get("deadline") or "TBD"].append(item)

    created_orders: List[Order] = []
    for deadline, grouped_items in grouped.items():
        order = Order(
            user_id=user_id,
            status="Pending",
            deadline=deadline,
            source_message=source_message,
        )
        db.add(order)
        db.flush()

        for item in grouped_items:
            db.add(
                OrderItem(
                    order_id=order.id,
                    product_name=item["product_name"],
                    category=item["category"],
                    quantity=item["quantity"],
                    specification=item["specification"],
                )
            )

        db.add(
            AnalyticsEvent(
                order_id=order.id,
                event_type="order_created",
                payload=json.dumps({"deadline": deadline, "items": grouped_items}),
            )
        )
        created_orders.append(order)

    db.commit()
    for order in created_orders:
        db.refresh(order)
    return created_orders


def update_order_status(db: Session, order: Order, status: str) -> Order:
    order.status = status
    db.add(
        AnalyticsEvent(
            order_id=order.id,
            event_type="status_updated",
            payload=json.dumps({"status": status}),
        )
    )
    db.commit()
    db.refresh(order)
    return order


def add_order_note(db: Session, order: Order, note: str) -> Order:
    db.add(
        AnalyticsEvent(
            order_id=order.id,
            event_type="quality_note",
            payload=json.dumps({"note": note}),
        )
    )
    db.commit()
    db.refresh(order)
    return order
