# configuracion de sqlmodel
from typing import Annotated
from fastapi import Depends  # para creacion de la dependencia
from sqlmodel import (
    Session,
    create_engine,
    SQLModel,
)  # permiten crear sesion para conectar a la base de datos
from fastapi import FastAPI


sqlite_name = "db.sqlite3"  # nombre de la base de datos
sqlite_url = f"sqlite:///{sqlite_name}"  # url de la base de datos

engine = create_engine(sqlite_url)

# creacion de tablas


def crate_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


def get_Sesion():
    with Session(engine) as session:  # crear sesion en la base de datos
        yield session


SessionDep = Annotated[
    Session, Depends(get_Sesion)
]  # Para usar la sesion dentro de los modelos a crear
