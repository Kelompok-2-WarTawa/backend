from .user_service import UserService
from .event_service import EventService
from .booking_service import BookingService


class ServiceContainer:
    def __init__(self, session):
        self.session = session

        self.user = UserService(session)
        self.event = EventService(session)
        self.booking = BookingService(session)
