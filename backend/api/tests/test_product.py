from fastapi.testclient import TestClient
from sqlmodel import Session

from models.table_models import Product


def get_dummy_product(i: int) -> Product:
    return Product(
        id=str(i), 
        name=f'prod{i}', 
        description=f'test{i}', 
        price=i*1000, 
        auther=f'auther{i}', 
        image_url=f'http://localhost{i}')


def test_read_products(session: Session, client: TestClient):
    resp = client.get(url='/api/products/')
    data: list[dict] = resp.json()
    assert resp.status_code == 200
    assert data == []

    for i in range(100):
        product = get_dummy_product(i=i)
        session.add(product)
    session.commit()

    resp = client.get(url='/api/products/')
    data = resp.json()
    assert len(data) == 20
    assert data == [get_dummy_product(i) for i in range(20)]

    resp = client.get(url='/api/products/', params={'skip': 0, 'limit': 120})
    data = resp.json()
    assert len(data) == 100
    assert data == [get_dummy_product(i) for i in range(100)]

    resp = client.get(url='/api/products/', params={'skip': 10, 'limit': 25})
    data = resp.json()
    assert len(data) == 25
    assert data == [get_dummy_product(i) for i in range(10, 10+25)]


def test_read_product(session: Session, client: TestClient):
    resp = client.get(url='/api/products/1')
    data: dict = resp.json()
    assert resp.status_code == 400
    assert data == {"detail": "Product not found"}

    for i in range(10):
        product = get_dummy_product(i=i)
        session.add(product)
    session.commit()

    resp = client.get(url='/api/products/1')
    data: dict = resp.json()
    assert resp.status_code == 200
    assert data == {
        'name': 'prod1',
        'description': 'test1',
        'price': 1000,
        'auther': 'auther1',
        'image_url': 'http://localhost1',
        'id': '1',
    }


