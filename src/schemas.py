from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional


class UserRegisterSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    nik: str = Field(..., min_length=16, max_length=16, pattern=r'^\d+$')
    phone_number: str = Field(..., min_length=10, max_length=15)


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class EventCreateSchema(BaseModel):
    name: str = Field(..., min_length=3)
    description: Optional[str] = ""
    date: str  # will parsed to datetime
    venue: str
    capacity: int = Field(..., gt=0)
    ticket_price: float = Field(..., ge=0)


class BookingCreateSchema(BaseModel):
    event_id: int
    quantity: int = Field(..., gt=0)


class PaymentSchema(BaseModel):
    amount: float = Field(..., gt=0)
    method: str
