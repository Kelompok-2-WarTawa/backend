from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from typing import List


class UserRegisterSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    nik: str = Field(..., min_length=16, max_length=16, pattern=r'^\d+$')
    phone_number: str = Field(..., min_length=10, max_length=15)


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class PhaseCreateSchema(BaseModel):
    name: str = Field(..., min_length=3)
    price: float = Field(..., ge=0)
    quota: int = Field(..., gt=0)
    start_date: str
    end_date: str

    @validator('end_date')
    def end_date_must_be_after_start(cls, v, values):
        if 'start_date' in values:
            start = datetime.fromisoformat(values['start_date'])
            end = datetime.fromisoformat(v)
            if end <= start:
                raise ValueError('End date must be after start date')
        return v


class EventCreateSchema(BaseModel):
    name: str = Field(..., min_length=3)
    description: Optional[str] = ""
    date: str
    venue: str
    phases: list[PhaseCreateSchema]

    @validator('date')
    def date_must_be_future(cls, v):
        try:
            dt = datetime.fromisoformat(v)
            if dt < datetime.now():
                raise ValueError('event date must be on the future')
            return v
        except ValueError as e:
            if "future" in str(e):
                raise e
            raise ValueError(
                'wrong date format. consider use ISO 8601 (YYYY-MM-DD HH:MM:SS)')


class BookingCreateSchema(BaseModel):
    event_id: int
    phase_id: int
    quantity: int = Field(..., gt=0)
    seat_ids: List[int]

    @validator('seat_ids')
    def validate_seats_match_quantity(cls, v, values):
        if 'quantity' in values and len(v) != values['quantity']:
            raise ValueError(f"the seats quantity ({len(
                v)}) bot same as booking quantity ({values['quantity']})")
        return v


class PaymentSchema(BaseModel):
    amount: float = Field(..., gt=0)
    method: str
