from sqlmodel import select
from models import Customer, Transaction, Transaction_create
from fastapi import APIRouter, HTTPException, Query, status
from db import SessionDep

router = APIRouter()


@router.post(
    "/transactions", tags=["Transactions"], status_code=status.HTTP_201_CREATED
)  # para crear una transaccion nueva
async def createtransaction(transaction_data: Transaction_create, session: SessionDep):
    transaction_data_dict = transaction_data.model_dump()
    customer = session.get(Customer, transaction_data_dict.get("customer_id"))
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The customer does not found to create a transaction",
        )
    transaction_db = Transaction.model_validate(
        transaction_data_dict
    )  # valida la informacion que estan brindando por tipo d datos
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    return transaction_db


@router.get("/transactions", tags=["Transactions"])
async def list_transaction(
    session: SessionDep,
    skip: int = Query(0, description="registros a omitir"),
    limit: int = Query(10, description="limite de registros a mostrar"),
):
    return session.exec(select(Transaction).offset(skip).limit(limit)).all() # se hace consulta con paginacion 
