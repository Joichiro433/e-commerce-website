from fastapi.testclient import TestClient
from sqlmodel import Session
import ulid
from rich import print

from models.table_models import Product, User, Order, OrderItem


dummy_ulids: list[str] = [str(ulid.new()) for _ in range(10)]


def append_dummy_data_to_table(session: Session):
    # product
    for i in range(10):
        product = Product(
            id=f'prod_id{i}',
            name=f'prod{i}', 
            description=f'test{i}', 
            price=i*1000, 
            auther=f'auther{i}', 
            image_url=f'http://localhost{i}')
        session.add(product)
    session.commit()
    # user
    user = User(id='user123456', email='dummy@example.com')
    session.add(user)
    session.commit()
    # order
    order = Order(id=dummy_ulids[0], user_id='user123456')
    session.add(order)
    session.commit()
    # order_item
    order_item1 = OrderItem(id=dummy_ulids[1], order_id=dummy_ulids[0], product_id='prod_id1', quantity=1)
    order_item2 = OrderItem(id=dummy_ulids[2], order_id=dummy_ulids[0], product_id='prod_id2', quantity=2)
    session.add(order_item1)
    session.add(order_item2)
    session.commit()
    
    
def get_dummy_product(i: int) -> Product:
    return Product(
        id=str(i), 
        name=f'prod{i}', 
        description=f'test{i}', 
        price=i*1000, 
        auther=f'auther{i}', 
        image_url=f'http://localhost{i}')


def get_dummy_user() -> User:
    return User(id='user123456', email='dummy@example.com')


def test_create_order(session: Session, client: TestClient):

    user = get_dummy_user()
    session.add(user)
    session.commit()
    for i in range(10):
        product = get_dummy_product(i=i)
        session.add(product)
    session.commit()

    resp = client.post(url='/api/orders/', json=[{'product_id': '1', 'quantity': 1}, {'product_id': '2', 'quantity': 2}])
    data: dict = resp.json()
    assert resp.status_code == 200
    assert data == {'message': 'Your order has been placed successfully.'}
    # resp = client.get(url='/api/orders/')
    # data: dict = resp.json()
    # print(data)
    # print(data.keys)



def test_read_orders(session: Session, client: TestClient):
    append_dummy_data_to_table(session=session)
    resp = client.get(url='/api/orders/')
    data: dict = resp.json()
    assert resp.status_code == 200

    expected_data = {
        'id': 'user123456',
        'email': 'dummy@example.com',
        'orders': [
            {
                'id': dummy_ulids[0],
                'order_items': [
                    {'quantity': 1, 'product': {'name': 'prod1', 'description': 'test1', 'price': 1000.0, 'auther': 'auther1', 'image_url': 'http://localhost1', 'id': 'prod_id1'}},
                    {'quantity': 2, 'product': {'name': 'prod2', 'description': 'test2', 'price': 2000.0, 'auther': 'auther2', 'image_url': 'http://localhost2', 'id': 'prod_id2'}}
                ]
            }
        ]
    }
    
    assert data == expected_data

