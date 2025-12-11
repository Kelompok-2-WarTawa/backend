from pyramid.view import view_config
from src.schemas import EventCreateSchema
from src.security import get_current_user_id


@view_config(route_name='events_list', request_method='GET', renderer='json')
def list_events(request):
    return request.services.event.get_all()


@view_config(route_name='events_detail', request_method='GET', renderer='json')
def get_event(request):
    event_id = int(request.matchdict['id'])
    return request.services.event.get_by_id(event_id)


@view_config(route_name='events_list', request_method='POST', renderer='json')
def create_event(request):
    user_id = get_current_user_id(request)

    payload = EventCreateSchema(**request.json_body)

    event = request.services.event.create(
        organizer_id=user_id, data=payload.dict())

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
