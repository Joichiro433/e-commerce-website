from collections.abc import Generator

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from firebase_admin import auth
from sqlmodel import Session, create_engine
from google.cloud.sql.connector import Connector, IPTypes
import redis
from redis import Redis

import settings
from models.table_models import *


class OAuth2PasswordBearerWithCookie(OAuth2PasswordBearer):
    """
    Extension of the OAuth2PasswordBearer class to support token retrieval from cookies.

    Parameters
    ----------
    tokenUrl : str
        The URL to get the token. This will be the URL to which the client's frontend will send the username and password, to get a token as a response.
    scheme_name : str, optional
        Custom name for the security scheme. Default is None.
    scopes : dict, optional
        A dictionary of valid scopes for this scheme. Default is None.
    auto_error : bool, optional
        Whether to raise exceptions automatically for invalid tokens. Default is True.

    Attributes
    ----------
    tokenUrl : str
        The URL to get the token.

    Methods
    -------
    __call__(request: Request) -> str | None
        Retrieve the token from cookie named "access_token" if available. Otherwise, fall back to the parent method.
    """
    def __init__(self, tokenUrl: str, scheme_name: str = None, scopes: dict = None, auto_error: bool = True):
        super(OAuth2PasswordBearerWithCookie, self).__init__(tokenUrl, scheme_name, scopes, auto_error)
        self.tokenUrl = tokenUrl

    def __call__(self, request: Request) -> str | None:
        """
        Retrieve the token from cookie named "access_token" if available. Otherwise, fall back to the parent method.

        Parameters
        ----------
        request : Request
            The incoming request instance.

        Returns
        -------
        str | None
            Token as a string if found, otherwise None.
        """
        cookie_token = request.cookies.get("access_token")
        if cookie_token:
            return cookie_token
        return super().__call__(request)
    
    
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl='api/login')
def verify_token(token = Depends(oauth2_scheme)) -> dict[str, str]:
    """
    Verify the provided OAuth2 token using Firebase's auth.verify_id_token.

    Parameters
    ----------
    token : str
        The OAuth2 token to be verified. This is obtained using the dependency `oauth2_scheme`.

    Returns
    -------
    dict[str, str]
        Decoded token if verification is successful.

    Raises
    ------
    HTTPException
        If token verification fails with any exception.
    """
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail=f'Unauthorized: {e}')


def getconn():
    """Cloud SQL Python Connector creator function"""
    connector = Connector()
    conn = connector.connect(
        settings.INSTANCE_CONNECTION_NAME,
        "pg8000",
        user=settings.DB_USER,
        password=settings.DB_PASS,
        db=settings.DB_NAME,
        ip_type=IPTypes.PRIVATE,
    )
    return conn

engine = create_engine("postgresql+pg8000://", creator=getconn, echo=True)
def get_session() -> Generator[Session, None, None]:
    """Returns a generator that can be used as a context manager to generate database sessions.

    Yields
    ------
    session : sqlmodel.Session
        The database session object.
    """
    with Session(engine) as session:
        yield session


redis_client = redis.StrictRedis(
    host=settings.REDIS_HOST, 
    port=settings.REDIS_PORT, 
    db=settings.REDIS_DB)
def get_redis_client() -> Redis:
    """
    Retrieve the Redis client instance.

    Returns
    -------
    Redis
        An instance of the Redis client.
    """
    return redis_client
