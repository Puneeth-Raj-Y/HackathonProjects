from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ORMBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserSchema(ORMBaseModel):
    id: int
    email: str
    role: str
    created_at: datetime


class OrderItemSchema(ORMBaseModel):
    id: int
    product_name: str
    category: str
    quantity: int
    specification: str


class OrderSchema(ORMBaseModel):
    id: int
    user_id: int
    status: str
    deadline: Optional[str] = None
    source_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemSchema] = Field(default_factory=list)


class AnalyticsEventSchema(ORMBaseModel):
    id: int
    order_id: Optional[int] = None
    event_type: str
    payload: str
    created_at: datetime


class ChatRequest(BaseModel):
    message: str
    user_id: int = 1


class ChatItemSchema(BaseModel):
    product_name: str
    category: str
    quantity: int
    specification: str
    deadline: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    intent: str
    extracted_items: List[ChatItemSchema] = Field(default_factory=list)
    created_orders: List[OrderSchema] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DashboardSummary(BaseModel):
    total_orders: int
    pending: int
    processing: int
    completed: int
    total_users: int
    recent_orders: List[OrderSchema] = Field(default_factory=list)


class StatusUpdateRequest(BaseModel):
    status: str


class QualityNoteRequest(BaseModel):
    note: str
