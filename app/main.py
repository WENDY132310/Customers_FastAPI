from typing import Annotated
from fastapi import  Depends, FastAPI, HTTPException, Request,status
from datetime import datetime
import zoneinfo, time

from fastapi.security import HTTPBasic, HTTPBasicCredentials
from db import crate_all_tables  # manejo de las bases de datos
from .routers import (
    customers,
    transactions,
    plans,
)  # importa las rutas de los endpoints
from sqlmodel import select


app = FastAPI(  # lifespan ejectuta metodo al inicio y final de app
    lifespan=crate_all_tables
)


app.include_router(
    customers.router
)  # se incluyen las rutas para customer de los endpoints
app.include_router(
    transactions.router
)  # se incluyen las rutas para transactions de los endpoints

app.include_router(plans.router)

@app.middleware("http")
async def log_request_time(request: Request, funcion):
    start_time= time.time()
    final_time= time.time() - start_time
    print(f"request {request.url} completed in : {final_time:4f} seconds")
    response = await funcion(request)
    return response
    
security=HTTPBasic()

@app.get("/")
async def root(credentials:Annotated [HTTPBasicCredentials,Depends(security)]):  #se usa autenticacion y autoriza los endpoints
    print(credentials)
    if credentials.username=="wen" and credentials.password=="123":  #validacion de credenciales para root
        
        return {"message": "Hola wendy"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f" user {credentials.username}  is not correct")


country_codes = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Peru",
}


@app.get(
    "/fecha/{codigo_pais}"
)  # Para agregar variables se coloca dentro de llaves el parametro a recibir para esta funcion, en este caso el codigo del pais
async def fecha(
    codigo_pais: str,
):  # Siempre se debe dar el tipo de dato de esta variable a recibir
    codigo = codigo_pais.upper()
    timezone_str = country_codes.get(codigo)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"la fecha en la ubicacion  " + timezone_str + " ": datetime.now(tz)}
