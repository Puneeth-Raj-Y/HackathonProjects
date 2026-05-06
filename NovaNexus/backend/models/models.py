from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default=UserRole.CUSTOMER)
    orders = relationship("Order", back_populates="customer")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="Pending") # Pending, Processing, Completed, Cancelled
    deadline = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    customer = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    quality_logs = relationship("QualityLog", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_name = Column(String)
    category = Column(String)
    quantity = Column(Integer)
    specification = Column(String)

    order = relationship("Order", back_populates="items")

class QualityLog(Base):
    __tablename__ = "quality_logs"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    note = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    order = relationship("Order", back_populates="quality_logs")

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String)
    response = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
