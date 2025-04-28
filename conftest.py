# PARA HACER PRUEBAS UNITARIAS

import pytest
from fastapi.testclient import TestClient  # permite consultar todos los metodos de http
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session
from app.main import app
from db import get_Sesion

sqlite_name = "db.sqlite3"  # nombre de la base de datos
sqlite_url = f"sqlite:///{sqlite_name}"  # url de la base de datos

engine = create_engine(
    sqlite_url, connect_args={"check_same_thread": False}, poolclass=StaticPool
)


@pytest.fixture(name="session")
def session_fixture():  # genera una nueva session para poder hacer pruebas
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def session_override():
        return session

    app.dependency_overrides[get_Sesion] = session_override #sobreescribe la sesion 
    client = TestClient(app)  # permite usar el client con sus modificaciones 
    yield client
    app.dependency_overrides.clear()
