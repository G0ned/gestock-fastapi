import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import get_db
from models import Base

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSession = sessionmaker(autocommit=False, bind=engine)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine) #Creación de las tablas de la base de datos vacías
    session = TestingSession()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine) #borrado de las tablas al finalizar el test

@pytest.fixture
def client(db):
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db #sustitución de la bd real
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def manufacturer(client):
    response = client.post("/manufacturers", json={
        "cif": "12345678Z",
        "name": "Logitech",
        "description": "Peripheral manufacturer",
        "email": "logitech_info@mail.text",
        "phone": "600000000"
    })
    # Si la creación falla, el test se detiene aquí mostrando la respuesta de la API
    assert response.status_code == 201, response.json()
    return response.json()