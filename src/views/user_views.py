from pyramid.view import view_config
from sqlalchemy import func
from src.schemas import UserRegisterSchema, UserLoginSchema
from src.security import create_access_token, login_required, admin_required
from src.utils import AuthorizationError
from src.models import Payment, Booking, Event


def user_response(user):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role.value,
        "phone_number": user.phone_number,
        "nik": user.nik
    }


@view_config(route_name='users_list', request_method='POST', renderer='json')
def register(request):
    payload = UserRegisterSchema(**request.json_body)
    user = request.services.user.create(
        name=payload.name,
        email=payload.email,
        password=payload.password,
    )
    user.nik = payload.nik
    user.phone_number = payload.phone_number
    request.dbsession.flush()

    request.response.status_code = 201
    return user_response(user)


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


@view_config(route_name='users_list', request_method='GET', renderer='json')
@admin_required
def list_users(request):
    users = request.services.user.get_all()
    return [user_response(u) for u in users]


@view_config(route_name='users_detail', request_method='GET', renderer='json')
@login_required
def get_user(request):
    target_id = int(request.matchdict['id'])

    from src.models import Role
    if request.user.role != Role.ADMIN and request.user.id != target_id:
        raise AuthorizationError("You cannot view other people's profile")

    user = request.services.user.get_by_id(target_id)
    return user_response(user)


@view_config(route_name='users_detail', request_method='PUT', renderer='json')
@login_required
def update_user(request):
    target_id = int(request.matchdict['id'])

    if request.user.id != target_id:
        raise AuthorizationError("You cannot edit other people's profile")

    data = request.json_body

    user = request.services.user.update(target_id, data)

    if 'nik' in data:
        user.nik = data['nik']
    if 'phone_number' in data:
        user.phone_number = data['phone_number']

    return user_response(user)


@view_config(route_name='users_detail', request_method='DELETE', renderer='json')
@admin_required
def delete_user(request):
    user_id = int(request.matchdict['id'])
    return request.services.user.delete(user_id)


@view_config(route_name='users_events', request_method='GET', renderer='json')
def get_user_created_events(request):
    user_id = int(request.matchdict['id'])
    return request.services.event.get_by_organizer(user_id)


@view_config(route_name='users_bookings', request_method='GET', renderer='json')
@login_required
def get_user_booking_history(request):
    target_id = int(request.matchdict['id'])

    if request.user.id != target_id:
        raise AuthorizationError("You cannot view other people's bookings")

    bookings = request.services.booking.get_by_customer(target_id)

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
                "venue": b.event.venue,
                "image_url": b.event.image_url
            }
        })
    return result


@view_config(route_name='admin_dashboard', request_method='GET', renderer='json')
@admin_required
def admin_dashboard(request):
    session = request.dbsession

    total_revenue = session.query(func.sum(Payment.amount))\
        .filter(Payment.status == 'success').scalar() or 0

    tickets_sold = session.query(func.sum(Booking.quantity))\
        .filter(Booking.status == 'confirmed').scalar() or 0

    active_events = session.query(func.count(Event.id)).scalar() or 0

    recent_tx_query = session.query(Booking)\
        .order_by(Booking.created_at.desc())\
        .limit(5)\
        .all()

    recent_transactions = [{
        "booking_code": b.booking_code,
        "user": b.customer.name,
        "amount": float(b.total_price),
        "status": b.status.value,
        "date": b.created_at.isoformat()
    } for b in recent_tx_query]

    return {
        "total_revenue": float(total_revenue),
        "tickets_sold": int(tickets_sold),
        "active_events": int(active_events),
        "recent_transactions": recent_transactions
    }
