from fastapi.testclient import TestClient
from main import get_application

def test_create_order():
    app = get_application()
    client = TestClient(app)
    response = client.post("/order", json={"name": "latte", "description": "yum", "price": 4.00})
    assert response.status_code == 200
    assert 'id' in response.json()

def test_rate_limiting():
    app = get_application()
    client = TestClient(app)
    for i in range(11):
        response = client.post("/order", json={"name": "latte", "description": "yum", "price": 4.00})
    assert response.status_code == 429
    assert 'Rate limit exceeded' in response.json()['error']

def test_get_order():
    app = get_application()
    client = TestClient(app)
    new_order = {"name": "latte", "description": "yum", "price": 4.00}
    create_resp = client.post("/order", json=new_order)
    assert create_resp.status_code == 200
    assert 'id' in create_resp.json()
    new_id = create_resp.json()["id"]

    get_resp = client.get(f"/orders/{new_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == new_order["name"]