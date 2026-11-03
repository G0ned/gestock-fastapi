from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models import ProductModel, ManufacturerModel
from schemas import ProductCreate, ProductRead
from database import get_db

# Inicialización de la aplicación
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=['*'],
)

@app.get('/')
def root():
    return {"Hello": "World"}

#Endpoints de productos
@app.get('/products', response_model=list[ProductRead])
def get_all_products(db:Session = Depends(get_db)):
    return db.query(ProductModel).all()


@app.get('/product/{id}', response_model=ProductRead)
def get_product_by_id(id: int, db:Session=Depends(get_db)):
    product = db.query(ProductModel).filter(ProductModel.id == id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post('/product', status_code=201, response_model=ProductRead)
def add_product(product: ProductCreate, db:Session=Depends(get_db)):
    new_product = ProductModel(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product
    
@app.put('/product/{id}', response_model=ProductRead)
def update_product(id: int, product: ProductCreate, db:Session=Depends(get_db)):
    updating_product = db.query(ProductModel).filter(ProductModel.id == id).first()
    if updating_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    updating_product.name  = product.name
    updating_product.description = product.description
    updating_product.price = product.price
    updating_product.quantity = product.quantity
    db.commit()
    return updating_product
        
@app.delete('/product/{id}', status_code=204)
def delete_product(id: int, db:Session=Depends(get_db)):
    deleting_product = db.query(ProductModel).filter(ProductModel.id == id).first()
    if deleting_product is None:
        raise HTTPException(status_code=404, detail="The product could not be deleted")
    db.delete(deleting_product)
    db.commit()

#Endpoints de fabricantes
@app.get('/manufacturers', status_code=200)
def get_all_manufacturers(db:Session=Depends(get_db)):
    pass

@app.get('/manufactuers/{manufacturer_id}', status_code=200)
def get_manufacturer(manufacturer_id: int, db:Session=Depends(get_db)):
    pass

@app.post('manufacturers', status_code=201)
def create_manufacturer(manufacturer: ManufacturerModel, db:Session=Depends(get_db)):
    pass