from db import engine
from sqlmodel import Session
from models import Transaction, Customer

session = Session(engine)
customer = Customer(
    name="Luis",
    descripcion="Estudiante",
    email="Luis@gmaiñ.com",
    age=21,
)

session.add(customer)
session.commit()

for x in range(100):
    session.add(
        Transaction(
            customer_id=customer.id, description=f"test de numero {x}", ammount=x * 10
        )
    )
    session.commit()


# este archivo crea 100  transacciones para el usuario que se esta creando
