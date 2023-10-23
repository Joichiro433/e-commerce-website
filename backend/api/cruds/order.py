from sqlmodel import select, Session
from sqlalchemy.orm import joinedload

from models.table_models import Order, OrderItem, User
from models.reqres_models import OrderItemCreate

def create_order(session: Session, user_id: str) -> Order:
    """
    Create a new order for a specific user.

    Parameters
    ----------
    session : Session
        The database session instance.
    user_id : str
        The ID of the user for whom the order is to be created.

    Returns
    -------
    Order
        The created order instance.
    """
    db_order: Order = Order(user_id=user_id)
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order

def create_order_item(session: Session, order_id: str, order_item: OrderItemCreate) -> OrderItem:
    """
    Create a new order item for a specific order.

    Parameters
    ----------
    session : Session
        The database session instance.
    order_id : str
        The ID of the order to which the order item is to be added.
    order_item : OrderItemCreate
        The data required to create the order item.

    Returns
    -------
    OrderItem
        The created order item instance.
    """
    db_order_item: OrderItem = OrderItem(
        order_id=order_id, 
        product_id=order_item.product_id, 
        quantity=order_item.quantity)
    session.add(db_order_item)
    session.commit()
    session.refresh(db_order_item)
    return db_order_item

def read_user_orders(session: Session, user_id: str):
    """
    Retrieve the orders associated with a specific user.

    Parameters
    ----------
    session : Session
        The database session instance.
    user_id : str
        The ID of the user whose orders are to be retrieved.

    Returns
    -------
    User
        The user instance with associated orders. (Note: In the provided code, orders and related 
        data are not eagerly loaded. You may need to uncomment the "joinedload" lines for complete data).
    """
    query = (
        select(User)
        .where(User.id == user_id)
        # .options(
        #     joinedload(User.orders)
        #     .joinedload(Order.order_items)
        #     .joinedload(OrderItem.product)
        # )
    )
    
    user = session.exec(query).first()
    return user
