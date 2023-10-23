from sqlmodel import select, Session, func
from models.table_models import Product

def read_product(session: Session, product_id: str) -> Product | None:
    """
    Retrieve a single product by its ID from the database.

    Parameters
    ----------
    session : Session
        The database session instance.
    product_id : str
        The ID of the product to retrieve.

    Returns
    -------
    Product | None
        The retrieved product instance, or None if not found.
    """
    product: Product | None = session.get(Product, product_id)
    return product

def read_products(session: Session, skip: int = 0, limit: int | None = 20) -> list[Product]:
    """
    Retrieve a list of products from the database with pagination.

    Parameters
    ----------
    session : Session
        The database session instance.
    skip : int, optional
        The number of products to skip before starting to fetch. Default is 0.
    limit : int, optional
        The maximum number of products to retrieve. Default is 20.

    Returns
    -------
    list[Product]
        A list of retrieved products.
    """
    query = select(Product).offset(skip).limit(limit)
    products: list[Product] = session.exec(query).all()
    return products

def count_products(session: Session) -> int:
    """
    Count the total number of products in the database.

    Parameters
    ----------
    session : Session
        The database session instance.

    Returns
    -------
    int
        The total number of products.
    """
    query = select(func.count(Product.id))
    total: int = session.exec(query).first()
    return total
