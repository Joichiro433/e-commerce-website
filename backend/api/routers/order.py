from typing import Annotated
import logging
from datetime import datetime

import ulid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

import cruds.order as order_crud
from models.table_models import Order, User
from models.reqres_models import OrderItemCreate, OrderRead, UserOrderRead, Message
from dependencies import get_session, verify_token


logger = logging.getLogger('uvicorn')

router = APIRouter(
    prefix='/orders',
    tags=['Order'],
    responses={404: {'message': 'Not found'}})


@router.post('', response_model=Message)
def create_order(
        session: Annotated[Session, Depends(get_session)],
        token: Annotated[dict, Depends(verify_token)],
        order_items: list[OrderItemCreate]
    ) -> Message:
    """
    Create a new order for the authenticated user.

    Parameters
    ----------
    **order_items** : list[OrderItemCreate], [body parameter]\n
        The items to be added to the order.

    Returns
    -------
    Message\n
        A success message indicating the order was placed.
    """
    user_id: str = token['uid']
    order: Order = order_crud.create_order(session=session, user_id=user_id)

    for order_item in order_items:
        order_crud.create_order_item(session=session, order_id=order.id, order_item=order_item)
    
    return {'message': 'Your order has been placed successfully.'}


@router.get('', response_model=UserOrderRead)
def read_orders(
        session: Annotated[Session, Depends(get_session)],
        token: Annotated[dict, Depends(verify_token)],
    ) -> UserOrderRead:
    """
    Retrieve all orders for the authenticated user.

    Returns
    -------
    UserOrderRead\n
        The user's orders with their details.
    """
    def _ulid_to_datetime(ulid_str: str) -> datetime:
        ulid_obj = ulid.parse(ulid_str)
        timestamp = ulid_obj.timestamp()
        dt = datetime.fromtimestamp(int(timestamp) / 1000.0)
        return dt

    user_id: str = token['uid']
    user_orders: User = order_crud.read_user_orders(session=session, user_id=user_id)
    order_read_list: list[OrderRead] = [OrderRead(id=order.id, order_items=order.order_items, purchase_date=_ulid_to_datetime(order.id)) for order in user_orders.orders]

    resp = UserOrderRead(id=user_orders.id, email=user_orders.email, orders=order_read_list)

    return resp
