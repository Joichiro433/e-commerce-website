from redis import Redis

from models.reqres_models import OrderItemCreate


def add_to_cart(redis_client: Redis, user_id: str, order_item: OrderItemCreate) -> None:
    """
    Adds an item to the user's cart in Redis. If the item's quantity is updated to 0 or less,
    the item is removed from the cart. The cart has a set expiry time.

    The function retrieves the user's cart from Redis using the user ID, then updates 
    the cart with the new item or updates the quantity of an existing item. It also 
    sets an expiry time for the cart to keep the Redis database uncluttered.

    Parameters
    ----------
    redis_client : Redis
        The Redis client instance to communicate with the Redis server. It is used to 
        get, update, and set the expiry time for the user's cart.
    user_id : str
        The unique identifier of the user. Used to retrieve the user's cart from Redis.
    order_item : OrderItemCreate
        An instance of OrderItemCreate that contains the product_id and quantity to be 
        added or updated in the user's cart.

    Returns
    -------
    None
        This function does not return a value; it updates the user's cart in Redis directly.
    """
    cart_key: str = f'cart:{user_id}'
    product_id: str = order_item.product_id
    quantity: int = order_item.quantity
    
    new_quantity: int = redis_client.hincrby(cart_key, product_id, quantity)
    if new_quantity <= 0:
        redis_client.hdel(cart_key, product_id)
    redis_client.expire(cart_key, 2 * 24 * 3600)


def update_cart_product(redis_client: Redis, user_id: str, order_item: OrderItemCreate) -> None:
    """
    Updates the quantity of a specific product in the user's cart in Redis. If the quantity is
    set to 0 or less, the product is removed from the cart. The function also updates the
    expiry time of the cart.

    Parameters
    ----------
    redis_client : Redis
        The Redis client instance used to communicate with the Redis server. It is utilized to 
        update the product quantity or remove the product from the cart and to reset the cart's 
        expiry time.
    user_id : str
        The unique identifier of the user, employed to pinpoint the specific user's cart in Redis.
    order_item : OrderItemCreate
        An instance containing the product_id and the new quantity to be set. If the quantity is 
        0 or less, the product is removed from the cart.

    Returns
    -------
    None
        The function doesn't return a value; it directly modifies the user's cart in Redis. The 
        cart is updated with the new quantity of the specified product, or the product is removed 
        if the quantity is 0 or less. The expiry time of the cart is also updated.

    Examples
    --------
    >>> update_cart_product(redis_client, 'user123', OrderItemCreate(product_id='product123', quantity=2))
    # This will set the quantity of 'product123' in the cart of 'user123' to 2 in Redis, and update the cart's expiry time.
    """
    cart_key: str = f'cart:{user_id}'
    product_id: str = order_item.product_id
    quantity: int = order_item.quantity

    if quantity <= 0:
        redis_client.hdel(cart_key, product_id)
    else:
        redis_client.hset(cart_key, product_id, quantity)
    redis_client.expire(cart_key, 2 * 24 * 3600)


def remove_from_cart(redis_client: Redis, user_id: str) -> None:
    """
    Remove all items from a user's cart.

    Parameters
    ----------
    redis_client : Redis
        The Redis client instance to communicate with the Redis server.
    user_id : str
        The unique identifier of the user.

    Returns
    -------
    None
    """
    cart_key: str = f'cart:{user_id}'
    redis_client.delete(cart_key)


def get_cart(redis_client: Redis, user_id: str) -> dict[str, int]:
    """
    Retrieve the contents of a user's cart.

    Parameters
    ----------
    redis_client : Redis
        The Redis client instance to communicate with the Redis server.
    user_id : str
        The unique identifier of the user.

    Returns
    -------
    dict[str, int]
        A dictionary where the keys are product_ids and the values are their quantities.
    """
    cart_key: str = f'cart:{user_id}'
    raw_cart = redis_client.hgetall(cart_key)
    return {k.decode('utf-8'): int(v) for k, v in raw_cart.items()}
