ERR_NOT_FOUND_PRODUCT = "Product not found"
ERR_NOT_FOUND_MANUFACTURER = "Manufacturer not found"


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
    assert response.json()["detail"] == ERR_NOT_FOUND_MANUFACTURER
    assert client.get("/products").json() == []


def test_updating_a_product(client, products):
    product = products[0]
    product_id = product["id"]
    product["quantity"] = 0
    response = client.put(f"/products/{product_id}", json=product)
    assert response.status_code == 200
    updated_product = client.get(f"/products/{product_id}").json()
    assert updated_product["quantity"] == 0
    assert updated_product["name"] == product["name"]
    assert updated_product["price"] == product["price"]


def test_updating_non_existent_product(client, manufacturer):
    product = {
        "name": "Headset",
        "description": "Headset with incorporated microphone and high-quality audio",
        "price": 79.99,
        "quantity": 10,
        "manufacturer_id": manufacturer["id"],
    }
    product_id = 999
    response = client.put(f"/products/{product_id}", json=product)
    assert response.status_code == 404
    assert response.json()["detail"] == ERR_NOT_FOUND_PRODUCT
    assert client.get("/products").json() == []


def test_updating_product_with_invalid_data(client, products):
    product = products[1]
    product_id = product["id"]
    price_before_up = product["price"]
    product["price"] = -20
    response = client.put(f"/products/{product_id}", json=product)
    error = response.json()["detail"][0]
    updated_product = client.get(f"/products/{product_id}").json()
    assert response.status_code == 422
    assert error["loc"] == ["body", "price"]
    assert error["type"] == "greater_than"
    assert updated_product["price"] == price_before_up


def test_updating_product_with_non_existent_manufacturer_id(client, products):
    product = products[0]
    manufacturer_id_before = product["manufacturer_id"]
    product_id = product["id"]
    product["manufacturer_id"] = 999
    response = client.put(f"/products/{product_id}", json=product)
    updated_product = client.get(f"/products/{product_id}").json()
    assert response.status_code == 404
    assert response.json()["detail"] == ERR_NOT_FOUND_MANUFACTURER
    assert updated_product["manufacturer_id"] == manufacturer_id_before


def test_delete_product(client, products):
    # Captación del ID de uno de los productos de prueba creados en conftest.py
    product_id = products[0]["id"]
    # Simulación de petición delete al endpoint correspondiente con el ID del producto guardado anteriormente
    response = client.delete(f"/products/{product_id}")
    # Comprobación de que el proceso de delete se produjo sin problemas y que el código de estado es 204
    assert response.status_code == 204
    # Comprobación de que el content de la respuesta está vacío ya que un delete
    # carece de contenido en el cuerpo de la respuesta
    assert response.content == b""
    # Simulación de una petición get del producto recién borrado usando el mismo id de producto
    get_del_product = client.get(f"/products/{product_id}")
    # Comprobación de que se devuelve un error 404 de que el producto no se pudo encontrar
    assert get_del_product.status_code == 404
    # Confirmación de que el error 404 es debido a que el producto no se pudo encontrar
    assert get_del_product.json()["detail"] == ERR_NOT_FOUND_PRODUCT
    # Ultima validación, que la eliminación de un producto no elimina los otros existentes
    assert len(client.get("/products/").json()) > 0


def test_delete_non_existent_product(client):
    # Invención de un ID de producto que no existe
    product_id = 999
    # Simulación de petición delete con ID que no existe
    response = client.delete(f"/products/{product_id}")
    # Comprobación de que devuelve un error 404 al no existir un producto con dicho ID
    assert response.status_code == 404
    # Confirmación de que la generación del error 404 es por la
    # petición debido a que no existe un producto con el ID indicado
    assert response.json()["detail"] == ERR_NOT_FOUND_PRODUCT


def test_delete_same_product_twice(client, products):
    # Captación del ID de uno de los productos de prueba creados en conftest.py
    product_id = products[1]["id"]
    # Simulación de petición delete
    response = client.delete(f"/products/{product_id}")
    # Comprobación de que el código de la respuesta es 204
    assert response.status_code == 204
    # Comprobación de que el content de la respuesta está vacío ya que un delete
    # carece de contenido en el cuerpo de la respuesta
    assert response.content == b""
    # Simulación de un intento de borrado del mismo producto
    second_del = client.delete(f"/products/{product_id}")
    # Comprobación de que el código de la respuesta es 404
    # y que se debe a que el producto no se ha encontrado
    assert second_del.status_code == 404
    assert second_del.json()["detail"] == ERR_NOT_FOUND_PRODUCT
