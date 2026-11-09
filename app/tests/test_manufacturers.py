ERR_NOT_FOUND_MANUFACTURER = "Manufacturer not found"


def get_id(data):
    return data["id"]


def test_list_manufacturer_empty(client):
    # Test para comprobar una query select cuando la base de datos está vacía funciona (codígo 200) pero no devuelve datos
    response = client.get("/manufacturers")
    assert response.status_code == 200
    assert response.json() == []


def test_list_manufacturers(client, manufacturer):
    # Test para comprobar que funciona la query select de todos los fabricantes
    response = client.get("/manufacturers")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_retrieve_manufacturer(client, manufacturer):
    # Test para comprobar que la query para consultar un fabricante concreto (ID: conocido) funciona correctamente
    manufacturer_id = get_id(manufacturer)
    response = client.get(f"/manufacturers/{manufacturer_id}")
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["name"] == "Logitech"


def test_retrieve_non_existen_manufacturer(client):
    # Test para comprobar que la consulta de un fabricante que no existe (ID inexistente) no funciona
    # (código 404 y error: fabricante no encontrado)
    manufacturer_id = 999
    response = client.get(f"/manufacturers/{manufacturer_id}")
    response_data = response.json()
    assert response.status_code == 404
    assert response_data["detail"] == ERR_NOT_FOUND_MANUFACTURER


def test_create_manufacturer(client):
    # Test para comprobar que la creación de un fabricante funciona
    # (código 201 y consulta posterior del fabricante recién creado)
    data = {
        "cif": "87654321A",
        "name": "Gigabyte",
        "description": "Hardware manufacturer",
        "email": "gigabyte_info@mail.text",
        "phone": "666666666",
    }

    response = client.post("/manufacturers", json=data)
    assert response.status_code == 201
    created_manufacturer = client.get("manufacturers").json()
    assert len(created_manufacturer) > 0
    assert created_manufacturer[0]["cif"] == data["cif"]


def test_create_manufacturer_with_repeated_cif(client, manufacturer):
    # Test para comprobar que no es posible crear un fabricante cuando el CIF está repetido
    # (código 409 y error: Manufacturer already exists)
    manufacturer_cif = manufacturer["cif"]
    data = {
        "cif": manufacturer_cif,
        "name": "Razer",
        "description": "Peripheral manufacturer",
        "email": "razer_info@mail.text",
        "phone": "666666666",
    }

    response = client.post("/manufacturers", json=data)
    response_data = response.json()
    assert response.status_code == 409
    assert response_data["detail"] == "Manufacturer already exists"
    assert len(client.get("/manufacturers").json()) == 1


def test_updating_manufacturer(client, manufacturer):
    # Test para comprobar que es posible actualizar los datos de un fabricante
    # (código: 200 y comprobación posterior de que los datos han sido actualizados)
    manufacturer_id = get_id(manufacturer)
    data = {
        "cif": "12345678Z",
        "name": "Logitech",
        "description": "Peripheral manufacturer",
        "email": "logitechinfo@mail.text",
        "phone": "123456789",
    }
    response = client.put(f"/manufacturers/{manufacturer_id}", json=data)
    assert response.status_code == 200
    updated_manufacturer = client.get(f"/manufacturers/{manufacturer_id}").json()
    assert updated_manufacturer["phone"] == data["phone"]
    assert updated_manufacturer["email"] == data["email"]


def test_updating_manufacturer_with_invalid_id(client, manufacturer):
    manufacturer = {
        "cif": "12345678Z",
        "name": "Logitech",
        "description": "Peripheral manufacturer",
        "email": "logitechinfo@mail.text",
        "phone": "111555666",
    }
    manufacturer["id"] = 999

    response = client.put(f"/manufacturers/{manufacturer['id']}", json=manufacturer)

    assert response.status_code == 404
    assert response.json()["detail"] == ERR_NOT_FOUND_MANUFACTURER


def test_updating_manufacturer_with_invalid_data(client, manufacturer):
    manufacturer_id = get_id(manufacturer)
    cif_before_update = manufacturer["cif"]
    manufacturer["cif"] = "123456789Z"

    response = client.put(f"/manufacturers/{manufacturer_id}", json=manufacturer)
    error = response.json()["detail"][0]
    assert response.status_code == 422
    assert error["loc"] == ["body", "cif"]
    assert error["type"] == "string_too_long"
    updated_product = client.get(f"/manufacturers/{manufacturer_id}").json()
    assert updated_product["cif"] == cif_before_update


def test_delete_manufacturer(client, manufacturer):
    manufacturer_id = get_id(manufacturer)

    response = client.delete(f"/manufacturers/{manufacturer_id}")
    assert response.status_code == 204
    assert client.get("/manufacturers").json() == []


def test_delete_manufacturer_does_not_affect_others(client, manufacturer):
    data = {
        "cif": "65874231H",
        "name": "AMD",
        "description": "Hardware manufacturer",
        "email": "amdeinfo@mail.text",
        "phone": "111333222",
    }
    creating = client.post("/manufacturers", json=data)

    manufacturer_id = creating.json()["id"]

    response = client.delete(f"/manufacturers/{manufacturer_id}")
    assert response.status_code == 204
    bd_data = client.get("/manufacturers").json()
    assert len(bd_data)
    assert bd_data[0]["cif"] == "12345678Z"


def test_delete_non_existent_manufacturer(client, manufacturer):
    response = client.delete(f"/manufacturers/{999}")
    assert response.status_code == 404
    assert response.json()["detail"] == ERR_NOT_FOUND_MANUFACTURER
    assert len(client.get("/manufacturers").json()) == 1
    assert client.get("/manufacturers").json()[0]["cif"] == "12345678Z"


def test_delete_same_manufacturer_twice(client, manufacturer):
    manufacturer_id = get_id(manufacturer)
    response = client.delete(f"/manufacturers/{manufacturer_id}")
    assert response.status_code == 204
    assert response.content == b""

    assert client.get("manufacturers").json() == []

    second_del = client.delete(f"/manufacturers/{manufacturer_id}")
    assert second_del.status_code == 404
    assert second_del.json()["detail"] == ERR_NOT_FOUND_MANUFACTURER
