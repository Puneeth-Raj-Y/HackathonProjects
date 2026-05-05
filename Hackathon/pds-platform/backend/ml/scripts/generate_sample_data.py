"""
Generate Sample Dataset for PDS Platform
"""
import sys
import os
from datetime import datetime, timedelta
import random

# Add paths
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from sqlalchemy.orm import Session
from database.db import SessionLocal, engine
from models import (
    Base, User, UserRole, Warehouse, Shop, StockTransaction,
    BeneficiaryTransaction, Grievance
)
from utils.auth_utils import hash_password


def generate_sample_data():
    """Generate sample data for testing"""
    print("Generating sample dataset...")

    db: Session = SessionLocal()

    # Create tables
    Base.metadata.create_all(bind=engine)

    # Clear existing data
    db.query(BeneficiaryTransaction).delete()
    db.query(StockTransaction).delete()
    db.query(Grievance).delete()
    db.query(Shop).delete()
    db.query(Warehouse).delete()
    db.query(User).delete()
    db.commit()

    # Create admin user
    admin = User(
        name="System Admin",
        unique_id="ADMIN123456",
        password=hash_password("admin_pass"),
        role=UserRole.ADMIN
    )
    db.add(admin)
    db.commit()
    print(f"[OK] Admin user created (ID: {admin.id})")

    # Create warehouses
    warehouses = [
        Warehouse(name="Central Warehouse", location="New Delhi"),
        Warehouse(name="North Warehouse", location="Punjab"),
        Warehouse(name="South Warehouse", location="Tamil Nadu"),
    ]
    db.add_all(warehouses)
    db.commit()
    print(f"[OK] {len(warehouses)} warehouses created")

    # Create shops
    shops = []
    for i in range(3):
        for j in range(2):
            shop = Shop(
                name=f"PDS Shop {i+1}-{j+1}",
                location=f"Location {i+1}-{j+1}",
                warehouse_id=warehouses[i].id,
                current_stock=random.uniform(200, 500)
            )
            shops.append(shop)
            db.add(shop)

    db.commit()
    print(f"[OK] {len(shops)} shops created")

    # Create stock transactions
    for warehouse in warehouses:
        for _ in range(5):
            transaction = StockTransaction(
                warehouse_id=warehouse.id,
                quantity=random.uniform(500, 2000),
                transaction_type='inbound',
                timestamp=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
                notes="Government supply"
            )
            db.add(transaction)

        for shop in [s for s in shops if s.warehouse_id == warehouse.id]:
            for _ in range(3):
                transaction = StockTransaction(
                    warehouse_id=warehouse.id,
                    shop_id=shop.id,
                    quantity=random.uniform(100, 300),
                    transaction_type='outbound',
                    timestamp=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
                    notes="Dispatch to shop"
                )
                db.add(transaction)

    db.commit()
    print(f"[OK] Stock transactions created")

    # Create beneficiary users and transactions
    beneficiaries = []
    for i in range(20):
        beneficiary = User(
            name=f"Beneficiary {i+1}",
            unique_id=f"BENEFICIARY{i:06d}",
            password=hash_password("beneficiary_pass"),
            role=UserRole.BENEFICIARY
        )
        db.add(beneficiary)
        db.flush()
        beneficiaries.append(beneficiary)

        # Create transactions for this beneficiary
        for _ in range(random.randint(3, 8)):
            transaction = BeneficiaryTransaction(
                user_id=beneficiary.id,
                shop_id=random.choice(shops).id,
                quantity=random.uniform(5, 25),
                timestamp=datetime.utcnow() - timedelta(days=random.randint(1, 30))
            )
            db.add(transaction)

    db.commit()
    print(f"[OK] {len(beneficiaries)} beneficiary users created with transactions")

    # Create shop users
    shop_users = []
    for i, shop in enumerate(shops):
        shop_user = User(
            name=f"Shop Manager {shop.name}",
            unique_id=f"SHOP{i:06d}",
            password=hash_password("shop_pass"),
            role=UserRole.SHOP
        )
        db.add(shop_user)
        shop_users.append(shop_user)

    db.commit()
    print(f"[OK] {len(shop_users)} shop users created")

    # Create grievances
    grievances_count = 0
    for beneficiary in beneficiaries[:15]:  # Some beneficiaries have grievances
        if random.random() > 0.5:  # 50% chance of having grievance
            grievance = Grievance(
                user_id=beneficiary.id,
                description=random.choice([
                    "Did not receive full quantity last time",
                    "Rude behavior from shop staff",
                    "Stock was expired",
                    "Long waiting time",
                    "Quantity mismatch"
                ]),
                status=random.choice(['open', 'resolved', 'closed']),
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 15))
            )
            db.add(grievance)
            grievances_count += 1

    db.commit()
    print(f"[OK] {grievances_count} grievances created")

    db.close()
    print("\n[SUCCESS] Sample dataset generation complete!")
    print(f"\nSample Data Summary:")
    print(f"  - Admin users: 1")
    print(f"  - Warehouses: {len(warehouses)}")
    print(f"  - Shops: {len(shops)}")
    print(f"  - Beneficiaries: {len(beneficiaries)}")
    print(f"  - Shop Managers: {len(shop_users)}")
    print(f"  - Grievances: {grievances_count}")


if __name__ == '__main__':
    generate_sample_data()
