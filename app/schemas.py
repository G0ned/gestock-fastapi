from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(max_length=500)
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)
    manufacturer_id: int


class ProductRead(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int
    manufacturer_id: (
        int | None
    )  # None para productos creados antes de existir los fabricantes

    model_config = {
        "from_attributes": True
    }  # Indica a Pydantic que se puede construir el JSON mediante los atributos. Por defecto intentaría acceder como un diccionario


class ManufacturerCreate(BaseModel):
    cif: str = Field(max_length=9)
    name: str
    description: str
    email: str
    phone: str


class ManufacturerRead(BaseModel):
    id: int
    cif: str = Field(max_length=9)
    name: str
    description: str
    email: str
    phone: str

    model_config = {"from_attributes": True}
