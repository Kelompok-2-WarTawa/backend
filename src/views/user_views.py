from pyramid.view import view_config
from src.schemas import UserRegisterSchema, UserLoginSchema
from src.security import create_access_token


def user_response(user):
    return {
        "id": user.id,
        "name": user.name,
        # i think email should be sanitized too
        # or no ?
        "email": user.email,
        "role": user.role.value
    }


@view_config(route_name='users_list', request_method='GET', renderer='json')
def list_users(request):
    users = request.services.user.get_all()
    return [user_response(u) for u in users]


@view_config(route_name='users_detail', request_method='GET', renderer='json')
def get_user(request):
    user_id = int(request.matchdict['id'])
    user = request.services.user.get_by_id(user_id)
    return user_response(user)


@view_config(route_name='users_list', request_method='POST', renderer='json')
def register(request):
    payload = UserRegisterSchema(**request.json_body)
    user = request.services.user.create(
        name=payload.name,
        email=payload.email,
        password=payload.password
    )
    request.response.status_code = 201

    return user_response(user)


@view_config(route_name='users_detail', request_method='PUT', renderer='json')
def update_user(request):
    user_id = int(request.matchdict['id'])
    data = request.json_body
    user = request.services.user.update(user_id, data)

    return user_response(user)


@view_config(route_name='users_detail', request_method='DELETE', renderer='json')
def delete_user(request):
    user_id = int(request.matchdict['id'])
    return request.services.user.delete(user_id)


@view_config(route_name='users_login', request_method='POST', renderer='json')
def login(request):
    payload = UserLoginSchema(**request.json_body)

    user = request.services.user.authenticate(
        email=payload.email,
        password=payload.password
    )

    token = create_access_token(user.id)

    return {
        "message": "Login successful",
        "token": token,
        "user": user_response(user)
    }


@view_config(route_name='users_events', request_method='GET', renderer='json')
def get_user_created_events(request):
    user_id = int(request.matchdict['id'])
    return request.services.event.get_by_organizer(user_id)


@view_config(route_name='users_bookings', request_method='GET', renderer='json')
def get_user_booking_history(request):
    user_id = int(request.matchdict['id'])
    bookings = request.services.booking.get_by_customer(user_id)

    result = []
    for b in bookings:
        result.append({
            "booking_code": b.booking_code,
            "status": b.status.value,
            "quantity": b.quantity,
            "total_price": float(b.total_price),
            "created_at": b.created_at.isoformat() if b.created_at else None,
            "event": {
                "id": b.event.id,
                "name": b.event.name,
                "date": b.event.date.isoformat(),
                "venue": b.event.venue
            }
        })
    return result
