from sqlalchemy import Column, Integer, String, Enum as SAEnum
from sqlalchemy.orm import relationship
from .base import Base, Role


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    role = Column(SAEnum(Role), default=Role.CUSTOMER)
    nik = Column(String(16), unique=True, nullable=True)
    phone_number = Column(String(20), nullable=True)

    events = relationship("Event", back_populates="organizer")
    bookings = relationship("Booking", back_populates="customer")
