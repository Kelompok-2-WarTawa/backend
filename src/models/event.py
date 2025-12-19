from sqlalchemy import (Column, Integer, String, DateTime,
                        Numeric, Text, ForeignKey, Enum as SAEnum)
from sqlalchemy.orm import relationship
from .base import Base, EventStatus


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    organizer_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    date = Column(DateTime, nullable=False)
    venue = Column(String(255), nullable=False)
    capacity = Column(Integer, nullable=False)
    ticket_price = Column(Numeric(10, 2), nullable=False)
    image_url = Column(String(255), nullable=True)
    status = Column(SAEnum(EventStatus), default=EventStatus.PUBLISHED)

    organizer = relationship("User", back_populates="events")
    bookings = relationship("Booking", back_populates="event")

    # Relasi ke Seat
    seats = relationship("Seat", back_populates="event",
                         cascade="all, delete-orphan")
