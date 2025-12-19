from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound
from src.schemas import EventCreateSchema
from src.security import get_current_user_id, admin_required
from src.models import Role, Seat, Event, TicketPhase
from src.utils import AuthorizationError
from sqlalchemy.orm import joinedload
from datetime import datetime


@view_config(route_name='events_list', request_method='GET', renderer='json')
def list_events(request):
    return request.services.event.get_all()


@view_config(route_name='events_detail', request_method='GET', renderer='json')
def get_event(request):
    event_id = int(request.matchdict['id'])

    event = request.dbsession.query(Event).\
        options(joinedload(Event.phases)).\
        get(event_id)

    if not event:
        raise HTTPNotFound()

    phases_data = []
    for p in event.phases:
        phases_data.append({
            "id": p.id,
            "name": p.name,
            "price": float(p.price),
            "quota": p.quota,
            "start_date": p.start_date.isoformat(),
            "end_date": p.end_date.isoformat(),
            "is_active": p.start_date <= datetime.now() <= p.end_date
        })

    return {
        "id": event.id,
        "organizer_id": event.organizer_id,
        "name": event.name,
        "description": event.description,
        "date": event.date.isoformat(),
        "venue": event.venue,
        "image_url": event.image_url,
        "total_capacity": event.capacity,
        "status": event.status.value,
        "phases": phases_data
    }


@view_config(route_name='events_seats', request_method='GET', renderer='json')
def get_event_seats(request):
    event_id = int(request.matchdict['id'])
    seats = request.dbsession.query(Seat).filter_by(
        event_id=event_id).order_by(Seat.id).all()

    return [{
        "label": s.seat_label,
        "is_booked": True if s.booking_id else False
    } for s in seats]


@view_config(route_name='events_list', request_method='POST', renderer='json')
@admin_required
def create_event(request):
    user_id = get_current_user_id(request)
    user = request.services.user.get_by_id(user_id)
    if user.role != Role.ADMIN:
        raise AuthorizationError("Only Admins can create events")

    payload = EventCreateSchema(**request.json_body)
    event = request.services.event.create(
        organizer_id=user.id,
        data=payload.dict()
    )
    request.response.status_code = 201
    return event


@view_config(route_name='events_detail', request_method='PUT', renderer='json')
@admin_required
def update_event(request):
    event_id = int(request.matchdict['id'])
    data = request.json_body
    return request.services.event.update(event_id, data)


@view_config(route_name='events_detail', request_method='DELETE', renderer='json')
@admin_required
def delete_event(request):
    event_id = int(request.matchdict['id'])
    return request.services.event.delete(event_id)
