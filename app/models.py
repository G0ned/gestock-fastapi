from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class ProductModel(Base):
    #Definición del nombre de la tabla
    __tablename__ = "products"
    #Definición de las columnas de la tabla y las restricciones correspondientes
    id = Column(Integer, name="id", primary_key=True, autoincrement=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    #Relación de la tabla productos con fabricante
    #Definición del tipo de dato y luego definición de llave foránea --> referencia a la columna de la otra tabla "nombre_tabla.campo"
    manufacturer_id = Column(Integer, ForeignKey("manufacturer.id"))
    manufacturer = relationship("ManufacturerModel", back_populates="products")

class ManufacturerModel(Base):
    __tablename__ = "manufacturer"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    cif = Column(String, unique=True)
    name = Column(String)
    description = Column(String)
    email = Column(String, unique=True)
    phone = Column(String, unique=True)
    
    products = relationship("ProductModel", back_populates="manufacturer")
    