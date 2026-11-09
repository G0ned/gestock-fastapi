import re
from typing import Annotated

from database import get_db
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import ManufacturerModel, ProductModel
from schemas import ManufacturerCreate, ManufacturerRead, ProductCreate, ProductRead
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

# Inicialización de la aplicación
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DbSession = Annotated[Session, Depends(get_db)]

ERR_NOT_FOUND_PRODUCT = "Product not found"
ERR_NOT_FOUND_MANUFACTURER = "Manufacturer not found"


def check_manufacturer_exists(manufacturer_id: int, db: Session):
    manufacturer = (
        db.query(ManufacturerModel)
        .filter(ManufacturerModel.id == manufacturer_id)
        .first()
    )
    if manufacturer is None:
        raise HTTPException(status_code=404, detail=ERR_NOT_FOUND_MANUFACTURER)

def check_email_format(email):
    regexp = r'^[A-Za-z][A-Za-z0-9_\.-]+@[A-Za-z0-9]+\.[a-z]{2,}$'

@app.get("/")
def root():
    return {"Hello": "World"}


# Endpoints de productos
@app.get("/products", response_model=list[ProductRead])
def get_all_products(db: DbSession):
    return db.query(ProductModel).all()


@app.get("/products/{id}", response_model=ProductRead)
def get_product_by_id(id: int, db: DbSession):
    product = db.query(ProductModel).filter(ProductModel.id == id).first()
    if product is None:
        raise HTTPException(status_code=404, detail=ERR_NOT_FOUND_PRODUCT)
    return product


@app.post("/products", status_code=201, response_model=ProductRead)
def add_product(product: ProductCreate, db: DbSession):
    check_manufacturer_exists(product.manufacturer_id, db)
    new_product = ProductModel(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.put("/products/{id}", response_model=ProductRead)
def update_product(id: int, product: ProductCreate, db: DbSession):
    updating_product = db.query(ProductModel).filter(ProductModel.id == id).first()
    if updating_product is None:
        raise HTTPException(status_code=404, detail=ERR_NOT_FOUND_PRODUCT)
    check_manufacturer_exists(product.manufacturer_id, db)
    updating_product.name = product.name
    updating_product.description = product.description
    updating_product.price = product.price
    updating_product.quantity = product.quantity
    updating_product.manufacturer_id = product.manufacturer_id
    db.commit()
    return updating_product


@app.delete("/products/{id}", status_code=204)
def delete_product(id: int, db: DbSession):
    deleting_product = db.query(ProductModel).filter(ProductModel.id == id).first()
    if deleting_product is None:
        raise HTTPException(status_code=404, detail=ERR_NOT_FOUND_PRODUCT)
    db.delete(deleting_product)
    db.commit()


# Endpoints de fabricantes
@app.get("/manufacturers", status_code=200)
def get_all_manufacturers(db: DbSession):
    return (db.query(ManufacturerModel)).all()


@app.get("/manufacturers/{manufacturer_id}", status_code=200)
def get_manufacturer(manufacturer_id: int, db: DbSession):
    manufacturer = (
        db.query(ManufacturerModel)
        .filter(ManufacturerModel.id == manufacturer_id)
        .first()
    )
    if manufacturer is None:
        raise HTTPException(status_code=404, detail="Manufacturer could not be found")
    else:
        return manufacturer


@app.post("/manufacturers", status_code=201)
def create_manufacturer(manufacturer: ManufacturerCreate, db: DbSession):
    new_manufacturer = ManufacturerModel(**manufacturer.model_dump())

    db.add(new_manufacturer)
    try:
        db.commit()
        db.refresh(new_manufacturer)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Manufacturer already exists")
    return new_manufacturer


@app.put("/manufacturers/{manufacturer_id}", response_model=ManufacturerRead)
def update_manufacturer(
    manufacturer_id: int,
    manufacturer: ManufacturerCreate,
    db: DbSession,
):
    updating_manufacturer = (
        db.query(ManufacturerModel)
        .filter(ManufacturerModel.id == manufacturer_id)
        .first()
    )
    if updating_manufacturer == None:
        raise HTTPException(status_code=404, detail=ERR_NOT_FOUND_MANUFACTURER)

    updating_manufacturer.name = manufacturer.name
    updating_manufacturer.cif = manufacturer.cif
    updating_manufacturer.description = manufacturer.description
    updating_manufacturer.email = manufacturer.email
    updating_manufacturer.phone = manufacturer.phone
    db.commit()
    return updating_manufacturer


@app.delete("/manufacturers/{manufacturer_id}", status_code=204)
def delete_manufacturer(manufacturer_id: int, db: DbSession):
    deleting_manufacturer = (
        db.query(ManufacturerModel)
        .filter(ManufacturerModel.id == manufacturer_id)
        .first()
    )
    if deleting_manufacturer == None:
        raise HTTPException(status_code=404, detail=ERR_NOT_FOUND_MANUFACTURER)
    db.delete(deleting_manufacturer)
    db.commit()
