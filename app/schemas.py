from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(max_length=500)
    price: float = Field(gt=0)
    quantity: int = Field(gt=0)
    