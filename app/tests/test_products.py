def test_list_products_empty(client):
    # Test para comprobar que una llamada cuando no hay datos en la bd funciona y devuelve json vacío
    response = client.get("/products")
    assert response.status_code == 200
    assert response.json() == []


def test_list_products(client, products):
    response = client.get("/products")
    assert response.status_code == 200
    response_data = response.json()
    # Comprobar que se devuelven exactamente los dos productos creados
    assert len(response_data) == 2
    assert [p["name"] for p in response_data] == ["Keyboard", "Headset"]


def test_get_product(client, products):
    product_id = products[0]["id"]
    print(product_id)
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == "Keyboard"


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
        "name": "Gaming Mouse",
        "description": "Gaming Mouse with up to 4800 dpi ideal for your competitive matches.",
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
        "name": "Hard Disk",
        "description": "Hard Disk with 2 TB of capacity",
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


def test_creating_product_with_invalid_manufacturer_id(client):
    data = {
        "name": "Computer case",
        "description": "Computer case with incorporated fans to help cooling",
        "price": 35.50,
        "quantity": 5,
        "manufacturer_id": 999,
    }

    response = client.post("/products", json=data)
    assert response.status_code == 404
    assert client.get("/products").json() == []


def test_updating_a_product(client, products):
    product = products[0]
    product_id = product["id"]
    product["quantity"] = 0
    response = client.put(f"/products/{product_id}", json=product)
    assert response.status_code == 200
    assert client.get(f"/products/{product_id}").json()["quantity"] == 0


def test_updating_non_existent_product(client, manufacturer):
    product = {
        "id": 999,
        "name": "Headset",
        "description": "Headset with incorporated microphone and high-quality audio",
        "price": 79.99,
        "quantity": 10,
        "manufacturer_id": manufacturer["id"],
    }
    product_id = product["id"]
    response = client.put(f"/products/{product_id}", json=product)
    assert response.status_code == 404


def test_updating_product_with_invalid_data(client, products):
    product = products[1]
    product_id = product["id"]
    product["price"] = -20
    response = client.put(f"/products/{product_id}", json=product)
    assert response.status_code == 422


def test_updating_product_with_non_existent_manufacturer_id(client, products):
    product = products[0]
    product_id = product["id"]
    product["manufacturer_id"] = 999
    response = client.put(f"/products/{product_id}", json=product)
    assert response.status_code == 404
