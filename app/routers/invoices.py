from sqlmodel import select
from models import Invoice
from fastapi import APIRouter
from db import SessionDep


router = APIRouter()


@router.post("/invoices")
async def createinvoice(invoice_data: Invoice):
    pass
