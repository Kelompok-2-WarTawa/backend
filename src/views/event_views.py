from pyramid.view import view_config
from src.schemas import EventCreateSchema
from src.security import get_current_user_id
from src.models import Role, Seat # Tambah Seat
from src.utils import AuthorizationError

@view_config(route_name='events_list', request_method='GET', renderer='json')
def list_events(request):
    return request.services.event.get_all()

@view_config(route_name='events_detail', request_method='GET', renderer='json')
def get_event(request):
    event_id = int(request.matchdict['id'])
    return request.services.event.get_by_id(event_id)

# --- VIEW BARU: LIHAT KURSI ---
@view_config(route_name='events_seats', request_method='GET', renderer='json')
def get_event_seats(request):
    event_id = int(request.matchdict['id'])
    # Ambil semua kursi dari event ini
    seats = request.dbsession.query(Seat).filter_by(event_id=event_id).order_by(Seat.id).all()
    
    # Return simple JSON
    return [{
        "label": s.seat_label,
        "is_booked": True if s.booking_id else False
    } for s in seats]

@view_config(route_name='events_list', request_method='POST', renderer='json')
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
def update_event(request):
    event_id = int(request.matchdict['id'])
    data = request.json_body
    return request.services.event.update(event_id, data)

@view_config(route_name='events_detail', request_method='DELETE', renderer='json')
def delete_event(request):
    event_id = int(request.matchdict['id'])
    return request.services.event.delete(event_id)