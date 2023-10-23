from typing import Annotated
import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
# from sentence_transformers import SentenceTransformer

import cruds.product as product_crud
from models.table_models import Product
from models.reqres_models import ProductRead, ProductCount
from dependencies import get_session
# from similarity_search.search_with_sentence_transformers import transformers_search


router = APIRouter(
    prefix='/products',
    tags=['Product'],
    responses={404: {'message': 'Not found'}})

logger = logging.getLogger('uvicorn')
# tf_model = SentenceTransformer('paraphrase-MiniLM-L6-v2', cache_folder='./cache_tf')


@router.get('', response_model=list[ProductRead])
def read_products(
        session: Annotated[Session, Depends(get_session)],
        skip: int = Query(0, ge=0),
        limit: int = Query(20, ge=1, le=100),
        query: str = Query('', max_length=200),
    ) -> list[ProductRead]:
    """
    Retrieve a list of products from the database. If a query is provided, products matching the query will be returned.

    Parameters
    ----------
    **skip** : int, optional, [query parameter]\n
        The number of products to skip before starting to return, by default 0.
    **limit** : int, optional, [query parameter]\n
        The maximum number of products to return, by default 20.
    **query** : str, optional, [query parameter]\n
        A search query string to filter products by.

    Returns
    -------
    list[ProductRead]\n
        A list of products.
    """
    if not query:
        return product_crud.read_products(session=session, skip=skip, limit=limit)
    else:
        return product_crud.read_products(session=session, skip=skip, limit=limit)
        # products: list[Product] = product_crud.read_products(session=session, skip=0, limit=None)
        # products, _ = transformers_search(model=tf_model, query=query, candidate_products=products)
        # return products[skip: skip+limit]
    

@router.get('/count', response_model=ProductCount)
def count_products(
        session: Annotated[Session, Depends(get_session)],
    ) -> ProductCount:
    """
    Count the total number of products in the database.

    Returns
    -------
    ProductCount\n
        The total number of products.
    """
    num_products: int = product_crud.count_products(session=session)
    return {'count': num_products}


@router.get('/{product_id}', response_model=ProductRead)
def read_product(
        session: Annotated[Session, Depends(get_session)],
        product_id: str,
    ) -> ProductRead:
    """
    Retrieve a specific product from the database by its ID.

    Parameters
    ----------
    **product_id** : str, [path parameter]\n
        The ID of the product to retrieve.

    Returns
    -------
    ProductRead\n
        The requested product.
    """
    product: Product | None = product_crud.read_product(session=session, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=400, detail='Product not found')
    return product
