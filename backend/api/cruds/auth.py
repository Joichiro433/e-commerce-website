from sqlmodel import select, Session
from models.table_models import User

def append_user(session: Session, user_id: str, email: str) -> User:
    """
    Add a new user to the database.

    Parameters
    ----------
    session : Session
        The database session instance.
    user_id : str
        The unique ID for the new user.
    email : str
        The email address of the new user.

    Returns
    -------
    User
        The created user instance.
    """
    db_user: User = User(id=user_id, email=email)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def get_user(session: Session, user_id: str) -> User | None:
    """
    Retrieve a user from the database by their unique ID.

    Parameters
    ----------
    session : Session
        The database session instance.
    user_id : str
        The unique ID of the user to be retrieved.

    Returns
    -------
    User | None
        The user instance if found, otherwise None.
    """
    user: User | None = session.get(User, user_id)
    return user

def delete_user(session: Session, db_user: User) -> None:
    """
    Remove a user from the database.

    Parameters
    ----------
    session : Session
        The database session instance.
    db_user : User
        The user instance to be removed.

    Returns
    -------
    None
    """
    session.delete(db_user)
    session.commit()
    return
