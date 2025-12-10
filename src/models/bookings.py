from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class Booking:
    id: int
    event_id: int
    attendee_id: int
    quantity: int
    total_price: Decimal
    booking_code: str
    booking_date: datetime
