from fastapi.testclient import TestClient


def test_add_to_cart(client: TestClient):
    resp = client.post(url='/api/cart/', json={'product_id': 'prod1', 'quantity': 1})
    data: dict = resp.json()
    assert resp.status_code == 200
    assert data == {'message': 'Item added to cart successfully.'}
    

def test_get_cart(client: TestClient):
    resp = client.get(url='/api/cart/')
    data: dict = resp.json()
    assert resp.status_code == 200
    assert data == {}

    client.post(url='/api/cart/', json={'product_id': 'prod1', 'quantity': 1})
    resp = client.get(url='/api/cart/')
    data: dict = resp.json()
    assert data == {'prod1': 1}

    client.post(url='/api/cart/', json={'product_id': 'prod2', 'quantity': 2})
    resp = client.get(url='/api/cart/')
    data: dict = resp.json()
    assert data == {'prod1': 1, 'prod2': 2}

    client.post(url='/api/cart/', json={'product_id': 'prod1', 'quantity': -1})
    client.post(url='/api/cart/', json={'product_id': 'prod2', 'quantity': 1})
    resp = client.get(url='/api/cart/')
    data: dict = resp.json()
    assert data == {'prod2': 3}

    client.post(url='/api/cart/', json={'product_id': 'prod1', 'quantity': -1})
    resp = client.get(url='/api/cart/')
    data: dict = resp.json()
    assert data == {'prod2': 3}


def test_remove_cart(client: TestClient):
    resp = client.delete(url='/api/cart/')
    data: dict = resp.json()
    assert resp.status_code == 200
    assert data == {'message': 'Item successfully removed from cart.'}

    client.post(url='/api/cart/', json={'product_id': 'prod1', 'quantity': 2})
    client.post(url='/api/cart/', json={'product_id': 'prod2', 'quantity': 3})
    resp = client.get(url='/api/cart/')
    data: dict = resp.json()
    assert data == {'prod1': 2, 'prod2': 3}
    client.delete(url='/api/cart/')
    resp = client.get(url='/api/cart/')
    data: dict = resp.json()
    assert data == {}
