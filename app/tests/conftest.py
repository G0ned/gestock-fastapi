import pytest
from database import get_db
from fastapi.testclient import TestClient
from main import app
from models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

engine = create_engine(
    "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
)

TestingSession = sessionmaker(autocommit=False, bind=engine)


@pytest.fixture
def db():
    Base.metadata.create_all(
        bind=engine
    )  # Creación de las tablas de la base de datos vacías
    session = TestingSession()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)  # borrado de las tablas al finalizar el test


@pytest.fixture
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db  # sustitución de la bd real
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def manufacturer(client):
    response = client.post(
        "/manufacturers",
        json={
            "cif": "12345678Z",
            "name": "Logitech",
            "description": "Peripheral manufacturer",
            "email": "logitech_info@mail.text",
            "phone": "600000000",
        },
    )
    # Si la creación falla, el test se detiene aquí mostrando la respuesta de la API
    assert response.status_code == 201, response.json()
    return response.json()


@pytest.fixture
def products(client, manufacturer):
    products_to_create = [
        {
            "name": "Keyboard",
            "description": "Keyboard for daily office work",
            "price": 12.99,
            "quantity": 100,
            "manufacturer_id": manufacturer["id"],
        },
        {
            "name": "Headset",
            "description": "Headset with incorporated microphone and high-quality audio",
            "price": 79.99,
            "quantity": 10,
            "manufacturer_id": manufacturer["id"],
        },
    ]
    created  = []
    for product in products_to_create:
        response = client.post("/products", json=product)
        assert response.status_code == 201, response.json()
        created.append(response.json())
    return created
