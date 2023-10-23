from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from redis import Redis

import cruds.cart as cart_crud
from dependencies import verify_token, get_redis_client
from models.reqres_models import OrderItemCreate, Message


router = APIRouter(
    prefix='/cart',
    tags=['Cart'],
    responses={404: {'message': 'Not found'}})


@router.post('', response_model=Message)
def add_to_cart(
        redis_client: Annotated[Redis, Depends(get_redis_client)],
        token: Annotated[dict, Depends(verify_token)],
        order_item: OrderItemCreate, 
    ) -> Message:
    """
    Add an item to the user's cart.

    Parameters
    ----------
    **order_item** : OrderItemCreate, [body parameter]\n
        The item to be added to the cart.

    Returns
    -------
    Message\n
        A success message indicating the item was added.
    """
    user_id: str = token['uid']
    try:
        cart_crud.add_to_cart(redis_client=redis_client, user_id=user_id, order_item=order_item)
        return {'message': 'Item added to cart successfully.'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put('', response_model=Message)
def update_cart_product(
        redis_client: Annotated[Redis, Depends(get_redis_client)],
        token: Annotated[dict, Depends(verify_token)],
        order_item: OrderItemCreate, 
    ) -> Message:
    """
    Update the quantity of an item in the user's cart.

    Parameters
    ----------
    **order_item** : OrderItemCreate, [body parameter]\n
        The item whose quantity is to be updated in the cart. 
        The `product_id` field indicates the product to be updated, 
        and the `quantity` field indicates the new quantity.

    Returns
    -------
    Message\n
        A success message indicating the item's quantity was updated successfully.
    """
    user_id: str = token['uid']
    try:
        cart_crud.update_cart_product(redis_client=redis_client, user_id=user_id, order_item=order_item)
        return {'message': 'Item quantity updated successfully.'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('', response_model=dict[str, int])
def get_cart(
        redis_client: Annotated[Redis, Depends(get_redis_client)],
        token: Annotated[dict, Depends(verify_token)],
    ):
    """
    Retrieve the user's cart contents.

    Returns
    -------
    dict[str, int]\n
        The contents of the user's cart with product IDs and their quantities.
        e.g., {"1111111": 1, "2111111": 3}
    """
    user_id: str = token['uid']
    cart_products: dict[str, int] = cart_crud.get_cart(redis_client=redis_client, user_id=user_id)
    return cart_products


@router.delete('', response_model=Message)
def remove_from_cart(
        redis_client: Annotated[Redis, Depends(get_redis_client)],
        token: Annotated[dict, Depends(verify_token)],
    ) -> Message:
    """
    Remove all items from the user's cart.

    Returns
    -------
    Message\n
        A success message indicating all items were removed.
    """
    user_id: str = token['uid']
    cart_crud.remove_from_cart(redis_client=redis_client, user_id=user_id)
    return {'message': 'Item successfully removed from cart.'}
