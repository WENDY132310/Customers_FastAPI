from enum import Enum
from db import engine
from pydantic import BaseModel, EmailStr, field_validator
from sqlmodel import (
    SQLModel,
    Relationship,
    Field,
    Session,
    select,
)  # permite crear modelos y conectarlos con la bse de datos, Field permite guardar variables en la bd


class StatusEnum(str, Enum):  # Estados que puede tener el plan
    ACTIVE = "active"
    INACTIVE = "inactive"


class CustomerPlan(SQLModel, table=True):  # relacion entre plan y customer
    id: int | None = Field(primary_key=True)
    plan_id: int = Field(foreign_key="plan.id")
    customer_id: int = Field(foreign_key="customer.id")
    status: StatusEnum = Field(
        default=StatusEnum.ACTIVE
    )  # por defecto el plan creado queda activo


class Plan(SQLModel, table=True):  # creacion de clase tipo plan
    id: int | None = Field(primary_key=True)
    nombre: str = Field(default=None)
    precio: int = Field(default=None)
    descripcion: str = Field(default=None)
    customers: list["Customer"] = Relationship(
        back_populates="plans", link_model=CustomerPlan
    )


class CustomerBase(SQLModel):  # Modelo de Customer

    name: str = Field(default=None)
    descripcion: str | None = Field(
        default=None
    )  # el simbolo | permite que la variable reciba varios tipos de datos
    email: EmailStr = Field(default=None)
    age: int = Field(default=None)

    @field_validator("email")  # decorador para hacer validacion de correo
    @classmethod
    def Validateemail(cls, value):
        session = Session(engine)
        result = session.exec(select(Customer).where(Customer.email == value)).first()
        if result:
            raise ValueError("This email is already resgistered in databases")
        return value


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    pass


class Customer(
    CustomerBase, table=True
):  # hereda de customer base y se crea una tabla en la bs para customer
    id: int | None = Field(
        default=None, primary_key=True
    )  # se asigna el tipo de dato relativo ya sea int o none y se define como PK en la base de datos
    transactions: list["Transaction"] = Relationship(back_populates="customer")
    plans: list[Plan] = Relationship(
        back_populates="customers", link_model=CustomerPlan
    )


class TransactionBase(SQLModel):
    ammount: int
    description: str


class Transaction_create(TransactionBase):
    customer_id: int = Field(foreign_key="customer.id")


class Transaction(TransactionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")  # creacion de llave foranea
    customer: Customer = Relationship(back_populates="transactions")


class Invoice(BaseModel):  # se conecta el modelo de customer y de transaction
    id: int
    customer: Customer
    transaction: list[Transaction]  # el usuario tendra una lista de transacciones
    total: int

    @property  # hace que sea accesible como una variable de clase
    def ammount_total(self):
        return sum(transaction.ammount for transaction in self.transactions)
