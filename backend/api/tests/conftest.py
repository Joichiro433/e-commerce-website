import sys
from pathlib import Path

app_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(app_dir))

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
import redis

from dependencies import get_session, verify_token, get_redis_client
from main import app


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        url="sqlite://",
        connect_args={"check_same_thread": False}, 
        poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    
    def verify_token_override():
        return {'uid': 'user123456'}
    
    def get_redis_client_override():
        redis_client = redis.StrictRedis(host='localhost', port=6379, db=1)
        return redis_client

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[verify_token] = verify_token_override
    app.dependency_overrides[get_redis_client] = get_redis_client_override
    client = TestClient(app)
    yield client
    get_redis_client_override().flushdb()
    app.dependency_overrides.clear()
    