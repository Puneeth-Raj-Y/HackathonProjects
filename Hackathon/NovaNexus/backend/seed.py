from database.db import SessionLocal, engine
from models import models

def seed_enterprise_data():
    db = SessionLocal()
    
    # Clear existing data
    db.query(models.ChatHistory).delete()
    db.query(models.QualityLog).delete()
    db.query(models.OrderItem).delete()
    db.query(models.Order).delete()
    db.query(models.User).delete()

    # Create Default Users
    customer = models.User(id=1, email="customer@forgemind.ai", hashed_password="pass", role="customer")
    admin = models.User(id=2, email="admin@forgemind.ai", hashed_password="pass", role="admin")
    db.add_all([customer, admin])
    db.commit()

    # Create Multi-Item Order
    order1 = models.Order(id=1, customer_id=1, status="Processing", deadline="July 20")
    db.add(order1)
    db.commit()

    items = [
        models.OrderItem(order_id=1, product_name="Workstation Laptop", category="Electronics", quantity=10, specification="i9, 32GB RAM"),
        models.OrderItem(order_id=1, product_name="Ergonomic Chair", category="Furniture", quantity=10, specification="Mesh, Lumbar Support")
    ]
    db.add_all(items)
    
    # Add Quality Log
    log = models.QualityLog(order_id=1, note="Hardware stress test passed. Furniture assembly verified.")
    db.add(log)
    
    db.commit()
    print("🚀 Enterprise data seeded successfully!")
    db.close()

if __name__ == "__main__":
    models.Base.metadata.create_all(bind=engine)
    seed_enterprise_data()
