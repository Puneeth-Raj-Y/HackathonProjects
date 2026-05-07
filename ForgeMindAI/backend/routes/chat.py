import logging
from collections import defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from models.schemas import ChatRequest, ChatResponse, OrderSchema
from nlp.engine import nlp_engine
from services.order_service import create_orders_from_items, order_to_dict

logger = logging.getLogger("forgemind.chat")
router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def post_chat(request: ChatRequest, db: Session = Depends(get_db)):
    logger.info("POST /api/chat user_id=%s message=%s", request.user_id, request.message)
    intent = nlp_engine.classify_intent(request.message)
    extracted_items = []
    created_orders = []
    reply = "I'm ready. Tell me what you need, for example: 'Need 100 bolts, 50 laptops, 20 medical kits'."

    try:
        if intent == "GREETING":
            reply = "Hello. I can extract multi-item orders, track status, and keep dashboards synchronized."
        elif intent == "CREATE_ORDER":
            extracted_items = nlp_engine.extract_items(request.message)
            created = create_orders_from_items(db, request.user_id, extracted_items, request.message)
            created_orders = [order_to_dict(order) for order in created]

            if len(created_orders) == 1:
                item_summary = nlp_engine.summarize_items(extracted_items)
                reply = f"Created order #{created_orders[0]['id']} for {item_summary}."
            else:
                order_ids = ", ".join(f"#{order['id']}" for order in created_orders)
                reply = f"Created {len(created_orders)} orders: {order_ids}."
        elif intent == "QUERY_STATUS":
            reply = "Share an order ID and I can look it up."
        else:
            reply = "I can help with orders. Try: 'Need 100 bolts, 50 laptops, 20 medical kits'."

        return ChatResponse(
            reply=reply,
            intent=intent,
            extracted_items=extracted_items,
            created_orders=created_orders,
            metadata={"user_id": request.user_id},
        )
    except Exception as exc:
        logger.exception("Chat request failed")
        return ChatResponse(
            reply="The request could not be processed right now. Please try again.",
            intent="ERROR",
            extracted_items=[],
            created_orders=[],
            metadata={"error": str(exc)},
        )
