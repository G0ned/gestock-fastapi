from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean
Base = declarative_base()

class ProductModel(Base):
    __tablename__ = "products"
    
    id = Column(Integer, name="id", primary_key=True, autoincrement=True, index=True)
    name = Column(String, name="name")
    description = Column(String, name="description")
    price = Column(Float, name="price")
    quantity = Column(Integer, name="quantity")