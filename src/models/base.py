from sqlalchemy.orm import declarative_base
import enum

Base = declarative_base()


class Role(str, enum.Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"


class BookingStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class PaymentStatus(str, enum.Enum):
    SUCCESS = "success"
    FAILED = "failed"
    REFUNDED = "refunded"


class EventStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ENDED = "ended"
