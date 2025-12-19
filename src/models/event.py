from sqlalchemy import (Column, Integer, String, DateTime,
                        Numeric, Text, ForeignKey, Enum as SAEnum)
from sqlalchemy.orm import relationship
from .base import Base, EventStatus


class TicketPhase(Base):
    __tablename__ = 'ticket_phases'
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)

    name = Column(String(50), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    quota = Column(Integer, nullable=False)

    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    event = relationship("Event", back_populates="phases")
    bookings = relationship("Booking", back_populates="phase")


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    organizer_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    date = Column(DateTime, nullable=False)
    venue = Column(String(255), nullable=False)

    capacity = Column(Integer, nullable=False)

    image_url = Column(Text, nullable=True)
    status = Column(SAEnum(EventStatus), default=EventStatus.PUBLISHED)

    organizer = relationship("User", back_populates="events")
    bookings = relationship("Booking", back_populates="event")
    seats = relationship("Seat", back_populates="event",
                         cascade="all, delete-orphan")

    phases = relationship(
        "TicketPhase", back_populates="event", cascade="all, delete-orphan")
