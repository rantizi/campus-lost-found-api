from app import create_app

def test_health_check():
    app = create_app()
    client = app.test_client()

    response = client.get("/health")
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["success"] is True
    assert json_data["data"]["status"] == "healthy"


def test_get_all_items():
    app = create_app()
    client = app.test_client()

    response = client.get("/api/items")
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["success"] is True
    assert isinstance(json_data["data"], list)


def test_create_item():
    app = create_app()
    client = app.test_client()

    new_item = {
        "name": "Kunci Motor",
        "category": "Key",
        "status": "found",
        "location": "Parkiran Gedung A",
        "description": "Kunci motor dengan gantungan merah",
        "contact": "081299999999"
    }

    response = client.post("/api/items", json=new_item)
    json_data = response.get_json()

    assert response.status_code == 201
    assert json_data["success"] is True
    assert json_data["data"]["name"] == "Kunci Motor"


def test_create_item_missing_field():
    app = create_app()
    client = app.test_client()

    invalid_item = {
        "name": "Jam Tangan"
    }

    response = client.post("/api/items", json=invalid_item)
    json_data = response.get_json()

    assert response.status_code == 400
    assert json_data["success"] is False


def test_get_item_not_found():
    app = create_app()
    client = app.test_client()

    response = client.get("/api/items/999")
    json_data = response.get_json()

    assert response.status_code == 404
    assert json_data["success"] is False