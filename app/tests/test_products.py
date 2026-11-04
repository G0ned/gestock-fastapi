def test_list_products_empty(client):
    # Test para comprobar que una llamada cuando no hay datos en la bd funciona y devuelve json vacío
    response = client.get("/products")
    assert response.status_code == 200
    assert response.json() == []


def test_list_products(client, manufacturer):
    products = [
        {
            "name": "Test Product",
            "description": "Product sample description",
            "price": 1,
            "quantity": 1,
            "manufacturer_id": manufacturer["id"],
        },
        {
            "name": "Test Product2",
            "description": "Product2 sample description",
            "price": 2,
            "quantity": 2,
            "manufacturer_id": manufacturer["id"],
        },
    ]

    for product in products:
        created = client.post("/products", json=product)
        # Si la creación falla, el test se detiene aquí mostrando el error de la API
        assert created.status_code == 201, created.json()

    response = client.get("/products")
    assert response.status_code == 200
    response_data = response.json()
    # Comprobar que se devuelven exactamente los dos productos creados
    assert len(response_data) == 2
    assert [p["name"] for p in response_data] == ["Test Product", "Test Product2"]

def test_create_product(client, manufacturer):
    # Test para comprobar que la creación de un producto funciona correctamente
    data = {
        "name": "Test Product",
        "description": "Product sample description",
        "price": 1,
        "quantity": 1,
        "manufacturer_id": manufacturer["id"],
    }

    response = client.post("/products", json=data)
    # Comprobar que el código de estado es 201
    assert response.status_code == 201
    response_data = response.json()
    # Comprobar que el ID no está vacío --> la autogeneración del ID es correcta
    assert response_data["id"] is not None
    # Comprobar que el nombre del producto es el mismo que el introducido
    assert response_data["name"] == "Test Product"
    # Comprobar que el ID del fabricante es el mismo que el introducido
    assert response_data["manufacturer_id"] == manufacturer["id"]


def test_create_product_with_negative_quantity(client, manufacturer):
    # Test para comprobar que no se puede crear un producto con un valor de cantidad negativo
    data = {
        "name": "Test Product2",
        "description": "Product2 sample description",
        "price": 1,
        "quantity": -5,
        "manufacturer_id": manufacturer["id"],
    }

    response = client.post("/products", json=data)
    response_data = response.json()
    # Comprobación que el código de error es 422
    assert response.status_code == 422
    error = response_data["detail"][0]
    # Confirmar que el error se produce por el campo correspondiente
    assert error["loc"] == ["body", "quantity"]  # comprobar qué campo ha fallado
    assert (
        error["type"] == "greater_than_equal"
    )  # comprobar qué regla ha fallado, en este caso (ge)
    # Comprobar que efectivamente no se ha creado ningún producto
    assert client.get("/products").json() == []


def test_create_product_with_price_equal_to_zero(client, manufacturer):
    # Test para comprobar que no se puede crear un producto si se introduce un precio igual a 0
    data = {
        "name": "Test Product3",
        "description": "Product3 sample description",
        "price": 0,
        "quantity": 100,
        "manufacturer_id": manufacturer["id"],
    }

    response = client.post("/products", json=data)
    response_data = response.json()

    assert response.status_code == 422
    error = response_data["detail"][0]
    assert error["loc"] == ["body", "price"]
    assert error["type"] == "greater_than"

    assert client.get("/products").json() == []


def test_create_product_with_negative_price(client, manufacturer):
    # Test para comprobar que no se puede crear un producto si se introduce un precio negativo
    data = {
        "name": "Test Product4",
        "description": "Product4 sample description",
        "price": -50,
        "quantity": 100,
        "manufacturer_id": manufacturer["id"],
    }

    response = client.post("/products", json=data)
    response_data = response.json()

    assert response.status_code == 422
    error = response_data["detail"][0]
    assert error["loc"] == ["body", "price"]
    assert error["type"] == "greater_than"

    assert client.get("/products").json() == []
