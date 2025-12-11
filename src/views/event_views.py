from pyramid.view import view_config


@view_config(route_name='events_list', request_method='GET', renderer='json')
def list_events(request):
    return request.services.event.get_all()


@view_config(route_name='events_detail', request_method='GET', renderer='json')
def get_event(request):
    event_id = int(request.matchdict['id'])
    return request.services.event.get_by_id(event_id)


@view_config(route_name='events_list', request_method='POST', renderer='json')
def create_event(request):
    data = request.json_body
    # organizer_id hardcoded as 1, because no middleware auth (jwt) yet
    event = request.services.event.create(organizer_id=1, data=data)
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
