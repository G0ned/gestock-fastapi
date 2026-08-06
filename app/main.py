from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models import ProductModel
from schemas import Product
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

@app.get('/products')
def get_all_products(db:Session = Depends(get_db)):
    products = db.query(ProductModel).all()
    if len(products) == 0:
        return {"Message": "No products could be found on the database."}
    else:
        return products

@app.get('/product/{id}')
def get_product_by_id(id: int, db:Session=Depends(get_db)):
    product = db.query(ProductModel).filter(ProductModel.id == id).first()
    if product:
        return product
    else:
        return {"Message":"The product could not be found..."}

@app.post('/product')
def add_product(product: Product, db:Session=Depends(get_db)):
    db.add(ProductModel(**product.model_dump()))
    db.commit()
    return product
    
@app.put('/product/{id}/update')
def update_product(id: int, product: Product, db:Session=Depends(get_db)):
    updating_product = db.query(ProductModel).filter(ProductModel.id == id).first()
    if updating_product:
        updating_product.name  = product.name
        updating_product.description = product.description
        updating_product.price = product.price
        updating_product.quantity = product.quantity
        db.commit()
        return {"Message": "Product updated successfully"}
    else:
        return {"Message": "The product could not be found. You can not update it..."}
        
@app.delete('/product/delete')
def delete_product(id: int, db:Session=Depends(get_db)):
    deleting_product = db.query(ProductModel).filter(ProductModel.id == id).first()
    if deleting_product:
        db.delete(deleting_product)
        db.commit()
        return {"Message": "Product deleted from the database succesfully."}
    else:
        return {"Message": "The product could not be found. You can not delete it..."}
            