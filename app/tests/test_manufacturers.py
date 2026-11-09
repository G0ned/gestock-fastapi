def test_list_manufacturer_empty(client):
    response = client.get("/manufacturers")
    assert response.status_code == 200
    assert response.json() == []

def test_list_manufacturers(client, manufacturer):
    response = client.get("/manufacturers")
    assert response.status_code == 200
    assert len(response.json()) > 0