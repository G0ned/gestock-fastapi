ERR_NOT_FOUND_MANUFACTURER = "Manufacturer could not be found"


def test_list_manufacturer_empty(client):
    response = client.get("/manufacturers")
    assert response.status_code == 200
    assert response.json() == []


def test_list_manufacturers(client, manufacturer):
    response = client.get("/manufacturers")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_retrieve_manufacturer(client, manufacturer):
    manufacturer_id = manufacturer["id"]
    response = client.get(f"/manufacturers/{manufacturer_id}")
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["name"] == "Logitech"


def test_retrieve_non_existen_manufacturer(client):
    manufacturer_id = 999
    response = client.get(f"/manufacturers/{manufacturer_id}")
    response_data = response.json()
    assert response.status_code == 404
    assert response_data["detail"] == ERR_NOT_FOUND_MANUFACTURER


def test_create_manufacturer(client):
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
    manufacturer_id = manufacturer["id"]
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
