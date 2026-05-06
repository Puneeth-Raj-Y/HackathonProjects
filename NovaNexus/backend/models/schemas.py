from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class UserBase(BaseModel):
    email: str
    role: str

class UserCreate(UserBase):
    password: str

class UserSchema(UserBase):
    id: int
    class Config:
        from_attributes = True

class OrderItemSchema(BaseModel):
    id: Optional[int]
    product_name: str
    category: str
    quantity: int
    specification: str
    class Config:
        from_attributes = True

class QualityLogSchema(BaseModel):
    id: int
    note: str
    timestamp: datetime
    class Config:
        from_attributes = True

class OrderSchema(BaseModel):
    id: int
    customer_id: int
    status: str
    deadline: str
    created_at: datetime
    items: List[OrderItemSchema]
    quality_logs: List[QualityLogSchema] = []
    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[int] = 1 # Default for demo

class ChatResponse(BaseModel):
    reply: str
    intent: str
    extracted_data: dict = {}
