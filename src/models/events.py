from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class Event:
    id: int
    organizer_id: int
    name: str
    description: str
    date: datetime
    venue: str
    capacity: int
    ticket_price: Decimal
