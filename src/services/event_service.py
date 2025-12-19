from datetime import datetime
from src.models import Event, Seat, TicketPhase
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
        if 'phases' not in data or not data['phases']:
            raise ValidationError("Event must have at least 1 ticket phase")

        phases_data = data.pop('phases')

        if isinstance(data.get('date'), str):
            try:
                data['date'] = datetime.fromisoformat(data['date'])
            except ValueError:
                raise ValidationError("Wrong format for event date")

        total_capacity = sum(p['quota'] for p in phases_data)
        data['capacity'] = total_capacity

        event = Event(organizer_id=organizer_id, **data)
        self.session.add(event)
        self.session.flush()

        for p_data in phases_data:
            phase = TicketPhase(
                event_id=event.id,
                name=p_data['name'],
                price=p_data['price'],
                quota=p_data['quota'],
                start_date=datetime.fromisoformat(p_data['start_date']),
                end_date=datetime.fromisoformat(p_data['end_date'])
            )
            self.session.add(phase)

        seats = []
        SEATS_PER_ROW = 10

        for i in range(total_capacity):
            row_idx = i // SEATS_PER_ROW

            col_num = (i % SEATS_PER_ROW) + 1

            row_char = chr(65 + row_idx)

            label = f"{row_char}{col_num}"

            seats.append(Seat(
                event_id=event.id,
                seat_label=label
            ))

        self.session.add_all(seats)
        return event

    def update(self, event_id, data):
        event = self.get_by_id(event_id)
        for key in ['name', 'description', 'venue', 'image_url']:
            if key in data:
                setattr(event, key, data[key])

        if 'date' in data:
            event.date = datetime.fromisoformat(data['date'])

        self.session.add(event)
        return event

    def delete(self, event_id):
        event = self.get_by_id(event_id)
        self.session.delete(event)
        return {"message": "Event deleted successfully"}

    def get_by_organizer(self, user_id):
        return self.session.query(Event).filter_by(organizer_id=user_id).all()
