from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from models import models, schemas
from nlp.engine import nlp_engine
from datetime import datetime

router = APIRouter(prefix="/api/chat", tags=["chat"])

@router.post("/", response_model=schemas.ChatResponse)
def handle_chat(request: schemas.ChatRequest, db: Session = Depends(get_db)):
    text = request.message
    intent = nlp_engine.classify_intent(text)
    
    reply = "I'm sorry, I couldn't process that. Try: 'Need 10 laptops and 5 chairs by Friday'."
    extracted_data = {}

    if intent == "GREETING":
        reply = "Hello! I'm ForgeMind Intelligence. I can help you manage orders across electronics, furniture, medical supplies, and more. How can I assist you today?"
    
    elif intent == "CREATE_ORDER":
        result = nlp_engine.parse_complex_request(text)
        items_to_create = result["items"]
        
        if items_to_create:
            orders_by_deadline = {}
            for item_data in items_to_create:
                dl = item_data.get("deadline", "TBD")
                if dl not in orders_by_deadline:
                    orders_by_deadline[dl] = []
                orders_by_deadline[dl].append(item_data)
                
            created_summaries = []
            order_ids = []
            
            for dl, items in orders_by_deadline.items():
                new_order = models.Order(
                    customer_id=request.user_id,
                    deadline=dl,
                    status="Pending"
                )
                db.add(new_order)
                db.commit()
                db.refresh(new_order)
                order_ids.append(new_order.id)
                
                item_strs = []
                for item_data in items:
                    item = models.OrderItem(
                        order_id=new_order.id,
                        product_name=item_data["product_name"],
                        category=item_data["category"],
                        quantity=item_data["quantity"],
                        specification=item_data["specification"]
                    )
                    db.add(item)
                    item_strs.append(f"{item.quantity}x {item.product_name}")
                
                db.commit()
                created_summaries.append(f"Order #{new_order.id} ({', '.join(item_strs)} by {dl})")
            
            reply = f"✅ Created: {'; '.join(created_summaries)}."
            extracted_data = {"order_ids": order_ids, "total_items": len(items_to_create)}
        else:
            reply = "I understood you want to place an order, but I couldn't identify the products or quantities. Please be specific, e.g., '10 office chairs'."

    elif intent == "QUERY_STATUS":
        result = nlp_engine.parse_complex_request(text)
        specific_id = result.get("order_id")
        
        if specific_id:
            order = db.query(models.Order).filter(models.Order.id == specific_id).first()
            if order:
                item_list = ", ".join([f"{i.quantity}x {i.product_name}" for i in order.items])
                reply = f"🔍 **Order #{order.id} Status**: {order.status}. Items: {item_list}. Deadline: {order.deadline}."
                
                latest_log = order.quality_logs[-1] if order.quality_logs else None
                if latest_log:
                    reply += f" 🛠️ **Quality Update**: '{latest_log.note}'"
                    
                extracted_data = {"order_id": order.id, "status": order.status}
            else:
                reply = f"❌ I couldn't find an order with ID #{specific_id} in our records."
        else:
            orders = db.query(models.Order).filter(models.Order.customer_id == request.user_id).order_by(models.Order.created_at.desc()).limit(3).all()
            if orders:
                order_list = ", ".join([f"#{o.id} ({o.status})" for o in orders])
                reply = f"📊 Found your recent orders: {order_list}. For details on a specific one, say 'Status of #4'."
            else:
                reply = "You don't have any orders yet. Would you like to create one?"

    return {
        "reply": reply,
        "intent": intent,
        "extracted_data": extracted_data
    }
