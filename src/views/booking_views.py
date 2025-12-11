from pyramid.view import view_config
from decimal import Decimal
from src.schemas import BookingCreateSchema, PaymentSchema
from src.security import get_current_user_id


@view_config(route_name='bookings_create', request_method='POST', renderer='json')
def create_booking(request):
    user_id = get_current_user_id(request)

    payload = BookingCreateSchema(**request.json_body)

    booking = request.services.booking.create_booking(
        customer_id=user_id,
        event_id=payload.event_id,
        quantity=payload.quantity
    )
    request.response.status_code = 201
    return booking


@view_config(route_name='bookings_detail', request_method='GET', renderer='json')
def get_booking(request):
    code = request.matchdict['code']
    return request.services.booking.get_booking(code)


@view_config(route_name='bookings_pay', request_method='POST', renderer='json')
def pay_booking(request):

    code = request.matchdict['code']
    payload = PaymentSchema(**request.json_body)

    return request.services.booking.pay_booking(
        booking_code=code,
        amount=payload.amount,
        method=payload.method
    )


@view_config(route_name='bookings_cancel', request_method='POST', renderer='json')
def cancel_booking(request):
    code = request.matchdict['code']
    return request.services.booking.cancel_booking(code)
