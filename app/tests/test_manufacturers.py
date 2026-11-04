def test_list_manufacturer_empty(client):
    response = client.get("/manufacturers")
    assert response.status_code == 200
    assert response.json() == []