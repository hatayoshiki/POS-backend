from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    jan_code = Column(String(13), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)

class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
