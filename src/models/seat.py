from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Seat(Base):
    __tablename__ = 'seats'
    
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    # booking_id NULL = Kursi Kosong. Terisi = Booked.
    booking_id = Column(Integer, ForeignKey('bookings.id'), nullable=True)
    
    seat_label = Column(String(10), nullable=False)  # Contoh: "A1", "B12"

    event = relationship("Event", back_populates="seats")
    booking = relationship("Booking", back_populates="seats")