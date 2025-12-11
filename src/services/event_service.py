from datetime import datetime
from src.models import Event
from src.utils import NotFound, ValidationError


class EventService:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Event).all()

    def get_by_id(self, event_id):
        event = self.session.query(Event).get(event_id)
        if not event:
            raise NotFound(f"Event ID {event_id} are not found")
        return event

    def create(self, organizer_id, data):
        if isinstance(data.get('date'), str):
            try:
                data['date'] = datetime.fromisoformat(data['date'])
            except ValueError:
                raise ValidationError(
                    "Wrong format. use ISO 8601 (YYYY-MM-DD HH:MM:SS)")

        event = Event(organizer_id=organizer_id, **data)
        self.session.add(event)
        self.session.flush()
        return event

    def update(self, event_id, data):
        event = self.get_by_id(event_id)

        for key in ['name', 'description', 'venue', 'capacity', 'ticket_price']:
            if key in data:
                setattr(event, key, data[key])

        if 'date' in data:
            if isinstance(data['date'], str):
                event.date = datetime.fromisoformat(data['date'])
            else:
                event.date = data['date']

        self.session.add(event)
        return event

    def delete(self, event_id):
        event = self.get_by_id(event_id)
        self.session.delete(event)
        return {"message": "Event deleted successfully"}
