from fastapi import APIRouter, Query, status, HTTPException
from sqlmodel import select
from models import (
    Customer,
    CustomerCreate,
    CustomerPlan,
    CustomerUpdate,
    Plan,
    StatusEnum,
)
from db import SessionDep


router = APIRouter()  # se generan los endpoints


@router.post(
    "/customers", response_model=Customer, tags=["Customers"], status_code=status.HTTP_201_CREATED
)  # Al consultar esta direccion responde con response_model
async def createcustomer(
    customer_data: CustomerCreate, session: SessionDep
):  # Este modelo crea customer en la bd
    customer = Customer.model_validate(
        customer_data.model_dump()
    )  # devuelve diccionario con todos los datos que esta ingresando el usuario
    session.add(customer)  # agrega el customer a la bd
    session.commit()  # hace el commit en la bd
    session.refresh(customer)  # refresca la variable en memoria

    return customer  # se devuelve la respuesta con el id incrementado


@router.get("/customers/{id_customer}", response_model=Customer, tags=["Customers"])
async def read_customer(customer_id: int, session: SessionDep):

    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer does not exist in bases",
        )  # genera mostrar errores
    return customer_db


@router.get(
    "/customers", response_model=list[Customer], tags=["Customers"]
)  # metodo para listar customers
async def listar_customers(session: SessionDep):
    return session.exec(
        select(Customer)
    ).all()  # se consulta la bd trayendo todos los customers y devuelve la lista


@router.delete("/Customers_Delete{id_customer}", tags=["Customers"])
async def Borrar_customer(Id_customer, session: SessionDep):
    customer_db = session.get(Customer, Id_customer)

    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="customer is not found to delete",
        )
    session.delete(customer_db)
    session.commit()
    return {"detail": "the process was succesful"}


@router.patch(
    "/customers/{id_customer}",
    response_model=Customer,
    status_code=status.HTTP_201_CREATED,
    description="It was modified succesful",
    tags=["Customers"],
)  # Hace modificacion del recurso de manera parcial
async def edit_customers(
    idcustomer: int, customer_data: CustomerUpdate, session: SessionDep
):
    customer_bd = session.get(Customer, idcustomer)
    if not customer_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The customer was not found in databases",
        )
    customerdata_dic = customer_data.model_dump(
        exclude_unset=True
    )  # toma los datos y los convierte en un diccionario excluyendo los datos que no brinda el usuario
    customer_bd.sqlmodel_update(customerdata_dic)  # se hace Query para actualizar
    session.add(customer_bd)
    session.commit()
    session.refresh(
        customer_bd
    )  # refresca la variable para mostrar los cambios realizados
    return customer_bd


@router.post(
    "/customers/{customer_id}/plans/{plan_id}", tags=["Subscriptions"]
)  # metodo para suscribir usuario a un plan
async def subscribe_customer_plan(
    customer_id: int,
    plan_id: int,
    session: SessionDep,
    plan_status: StatusEnum = Query(),
):
    customer_db = session.get(Customer, customer_id)
    plan_db = session.get(Plan, plan_id)

    if (
        not plan_db or not customer_db
    ):  # se valida la existencia del customer y del plan
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The plan or customer doesn't exist in databases",
        )
    customerplan_db = CustomerPlan(
        plan_id=plan_db.id, customer_id=customer_db.id, status=plan_status
    )  # se llama a la relacion para la base de datos en models
    session.add(customerplan_db)
    session.commit()
    session.refresh(customerplan_db)
    return customerplan_db


@router.get(
    "/customers/{customer_id}/plans/", tags=["Subscriptions"]
)  # metodo para listar un usuario y un plan
async def list_customer_plan(
    customer_id: int, session: SessionDep, status: StatusEnum = Query()
):
    customer_bd = session.get(Customer, customer_id)
    plans = session.exec(
        select(CustomerPlan)
        .where(CustomerPlan.customer_id == customer_id)
        .where(CustomerPlan.status == status)
    ).all()
    if not customer_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The customer doesnt exist in databases",
        )
    return plans
