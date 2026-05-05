"""
Database Models for PDS Platform
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class UserRole(enum.Enum):
    """User roles in the system"""
    ADMIN = "admin"
    SHOP = "shop"
    BENEFICIARY = "beneficiary"


class User(Base):
    """User model for authentication and role-based access"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    unique_id = Column(String(50), unique=True, nullable=False)  # Aadhaar-like ID
    password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    grievances = relationship('Grievance', back_populates='user')
    beneficiary_transactions = relationship('BeneficiaryTransaction', back_populates='user')

    def __repr__(self):
        return f"<User {self.name} ({self.role.value})>"


class Warehouse(Base):
    """Warehouse model for storing bulk goods"""
    __tablename__ = 'warehouses'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    location = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    shops = relationship('Shop', back_populates='warehouse')
    stock_transactions = relationship('StockTransaction', back_populates='warehouse')

    def __repr__(self):
        return f"<Warehouse {self.name}>"


class Shop(Base):
    """Shop model for PDS distribution points"""
    __tablename__ = 'shops'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    location = Column(String(255), nullable=False)
    warehouse_id = Column(Integer, ForeignKey('warehouses.id'), nullable=False)
    current_stock = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    warehouse = relationship('Warehouse', back_populates='shops')
    beneficiary_transactions = relationship('BeneficiaryTransaction', back_populates='shop')
    stock_transactions = relationship('StockTransaction', back_populates='shop')

    def __repr__(self):
        return f"<Shop {self.name}>"


class StockTransaction(Base):
    """Model for tracking stock movements between warehouses and shops"""
    __tablename__ = 'stock_transactions'

    id = Column(Integer, primary_key=True)
    warehouse_id = Column(Integer, ForeignKey('warehouses.id'), nullable=False)
    shop_id = Column(Integer, ForeignKey('shops.id'), nullable=True)
    quantity = Column(Float, nullable=False)
    transaction_type = Column(String(20), nullable=False)  # 'inbound', 'outbound'
    timestamp = Column(DateTime, default=datetime.utcnow)
    notes = Column(String(500), nullable=True)

    # Relationships
    warehouse = relationship('Warehouse', back_populates='stock_transactions')
    shop = relationship('Shop', back_populates='stock_transactions')
    fraud_alerts = relationship('FraudAlert', back_populates='transaction')

    def __repr__(self):
        return f"<StockTransaction {self.id}>"


class BeneficiaryTransaction(Base):
    """Model for tracking beneficiary distributions"""
    __tablename__ = 'beneficiary_transactions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    shop_id = Column(Integer, ForeignKey('shops.id'), nullable=False)
    quantity = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship('User', back_populates='beneficiary_transactions')
    shop = relationship('Shop', back_populates='beneficiary_transactions')
    fraud_alerts = relationship('FraudAlert', back_populates='beneficiary_transaction')

    def __repr__(self):
        return f"<BeneficiaryTransaction {self.id}>"


class Grievance(Base):
    """Model for tracking user grievances"""
    __tablename__ = 'grievances'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    description = Column(String(1000), nullable=False)
    status = Column(String(20), default='open')  # open, resolved, closed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship('User', back_populates='grievances')

    def __repr__(self):
        return f"<Grievance {self.id}>"


class FraudAlert(Base):
    """Model for fraud detection alerts"""
    __tablename__ = 'fraud_alerts'

    id = Column(Integer, primary_key=True)
    stock_transaction_id = Column(Integer, ForeignKey('stock_transactions.id'), nullable=True)
    beneficiary_transaction_id = Column(Integer, ForeignKey('beneficiary_transactions.id'), nullable=True)
    reason = Column(String(500), nullable=False)
    risk_score = Column(Float, nullable=False)  # 0-1
    is_anomaly = Column(Integer, default=0)  # 1 if anomaly detected
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    transaction = relationship('StockTransaction', back_populates='fraud_alerts')
    beneficiary_transaction = relationship('BeneficiaryTransaction', back_populates='fraud_alerts')

    def __repr__(self):
        return f"<FraudAlert {self.id}>"
