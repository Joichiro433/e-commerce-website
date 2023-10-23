import os
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
import firebase_admin
from firebase_admin._user_mgt import UserRecord
from firebase_admin import credentials, auth
import pyrebase
from pyrebase.pyrebase import Auth
from sqlmodel import Session
import logging

import cruds.auth as auth_crud
from models.reqres_models import SignUpCreate, UserRead, Message
from dependencies import verify_token, get_session
from models.table_models import User
import settings


cred = credentials.Certificate(settings.FIREBASE_AUTH)
firebase_admin.initialize_app(cred)
firebase_auth: Auth = pyrebase.initialize_app(settings.FIREBASE_CONFIG).auth()

logger = logging.getLogger('uvicorn')

router = APIRouter(
    prefix='',
    tags=['Auth'],
    responses={404: {'message': 'Not found'}})


token_store: dict[str, str] = {}


@router.post('/signup', response_model=Message)
def create_account(
        session: Annotated[Session, Depends(get_session)],
        user_data: SignUpCreate,
    ) -> Message:
    """
    Create a new user account.

    This function will create a new user record in the authentication system and also
    store user details in the database. If an account with the given email already exists, 
    the function will raise an error.

    Parameters
    ----------
    **user_data** : SignUpCreate, [body parameter]\n
        The user's sign-up data, containing the email and password.

    Returns
    -------
    dict[str, str]\n
        A dictionary containing a message about the successful creation of the account.

    Raises
    ------
    HTTPException\n
        If an account with the given email already exists.
    """
    email: str = user_data.email
    password: str = user_data.password

    try:
        user: UserRecord = auth.create_user(email=email, password=password)
        user_id: str = user.uid
        auth_crud.append_user(session=session, user_id=user_id, email=email)
        return {'message': f'Account created successfully for user {user_id}'}
    except auth.EmailAlreadyExistsError:
        raise HTTPException(
            status_code=400, 
            detail=f'Account already created for the email {email}')


@router.post('/login', response_model=Message)
def create_access_token(
        user_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
        response: Response
    ) -> Message:
    """
    Authenticate a user and set an access token in a cookie.

    This function attempts to authenticate a user using their email and password with Firebase.
    If authentication is successful, the function will set an access token as an HTTP-only cookie 
    in the client's browser. If authentication fails, the function will raise an error.

    Parameters
    ----------
    **user_data** : OAuth2PasswordRequestForm, [body parameter]\n
        The user's login data, containing the username (email) and password.

    Returns
    -------
    dict[str, str]\n
        A dictionary containing a message indicating that the user was successfully logged in 
        and the token was set in the cookie.

    Raises
    ------
    HTTPException\n
        If there was an issue logging in the user.
    """
    email: str = user_data.username
    password: str = user_data.password

    try:
        user_logged: dict = firebase_auth.sign_in_with_email_and_password(
            email=email,
            password=password)
        token: str = user_logged['idToken']
        refresh_token: str = user_logged['refreshToken']
        token_store['refresh_token'] = refresh_token

        response.set_cookie(
            key="access_token", 
            value=token, 
            httponly=True,
            max_age=3600,
            samesite='none',
            secure=True
        )
        
        return {"message": "Logged in and token set in cookie"}
    
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f'Could not login: {e}')
    

@router.post('/logout', response_model=Message)
def logout(response: Response) -> Message:
    """
    Log out the user by removing the access token from the cookie.

    This function deletes the "access_token" cookie from the client's browser, effectively logging out 
    the user from the application. If the cookie does not exist, no error will be thrown and the function 
    will continue its operation normally.

    Returns
    -------
    dict[str, str]\n
        A dictionary containing a message indicating that the user was successfully logged out and 
        the token was removed from the cookie.
    """
    response.delete_cookie("access_token")
    return {"message": "Logged out and token removed from cookie"}
    

@router.get('/refresh')
def refresh_access_token(token: Annotated[dict, Depends(verify_token)]):
    refresh_token = token_store.get('refresh_token')
    if refresh_token is None:
        raise HTTPException(
            status_code=400,
            detail=f'refresh_token is None')
    
    user = firebase_auth.refresh(refresh_token)
    token: str = user['idToken']

    logger.info(f'refresh token: {token_store}')

    return {"access_token": token, "token_type": "bearer"}
    

@router.get('/is-logged-in')
def is_logged_in(request: Request):
    # access_tokenの確認を行います
    token = request.cookies.get("access_token")
    logger.info(token)
    if not token:
        return {"isLoggedIn": False}
    
    try:
        auth.verify_id_token(token)
        return {"isLoggedIn": True}
    except:
        return {"isLoggedIn": False}


@router.get('/ping')
def validate_token(token: Annotated[dict, Depends(verify_token)]):
    return {"user_id": token["uid"]}


@router.get('/user', response_model=UserRead)
def read_user(
        session: Annotated[Session, Depends(get_session)],
        token: Annotated[dict, Depends(verify_token)],
    ) -> UserRead:
    """
    Retrieve user details from the database using the user's ID.

    This function fetches user details based on the user ID extracted from the provided token.
    If the user is not found in the database, a 400 HTTP status code is returned with a "User not found" message.

    Returns
    -------
    UserRead\n
        The retrieved user details.

    Raises
    ------
    HTTPException\n
        If the user is not found in the database.
    """
    user_id: str = token['uid']
    user: User | None = auth_crud.get_user(session=session, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=400, detail='User not found')
    return user


@router.delete('/user', response_model=Message)
def delete_user(
        session: Annotated[Session, Depends(get_session)],
        token: Annotated[dict, Depends(verify_token)],
    ) -> Message:
    """
    Delete the user's account and associated data from the database.

    This function removes a user's account based on the user ID extracted from the provided token.
    First, it checks if the user exists in the database. If not, a 400 HTTP status code is returned with a "User not found" message.
    If the user exists, the function attempts to delete the user's account and any associated data.
    If there's any problem in the deletion process, a 400 HTTP status code is returned with a detailed error message.

    Returns
    -------
    dict : [str, str]\n
        A json response indicating the status of the deletion operation.

    Raises
    ------
    HTTPException\n
        If the user is not found in the database or there's any problem during the deletion process.
    """
    user_id: str = token['uid']
    user: User | None = auth_crud.get_user(session=session, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=400, detail='User not found')
    
    try:
        auth.delete_user(uid=user_id)
        auth_crud.delete_user(session=session, db_user=user)
        return {"message": "User successfully deleted."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not delete user: {e}")
