from pyramid.view import view_config
from src.schemas import BookingCreateSchema, PaymentSchema
from src.security import get_current_user_id
from src.models import Role
from src.utils import AuthorizationError


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


@view_config(route_name='bookings_checkin', request_method='POST', renderer='json')
def scan_ticket(request):
    # Admin check (masa penonton scan sendiri?)
    user_id = get_current_user_id(request)
    user = request.services.user.get_by_id(user_id)

    if user.role != Role.ADMIN:
        raise AuthorizationError("Hanya panitia (Admin) yang boleh scan tiket")

    code = request.matchdict['code']
    return request.services.booking.check_in_ticket(code)


@view_config(route_name='bookings_detail', request_method='GET', renderer='json')
def get_booking(request):
    code = request.matchdict['code']
    booking = request.services.booking.get_booking(code)

    fake_va = f"8800{booking.customer_id:04d}{booking.id:04d}"

    payment_method_display = "Virtual Account (BCA/Mandiri/BRI)"

    if booking.payment:
        payment_method_display = booking.payment.method.upper()

    return {
        "booking_code": booking.booking_code,
        "event_name": booking.event.name,
        "quantity": booking.quantity,
        "total_price": float(booking.total_price),
        "status": booking.status.value,

        "seat_labels": [s.seat_label for s in booking.seats],

        "payment_info": {
            "virtual_account": fake_va,
            "bank": payment_method_display,
            "qr_string": booking.booking_code
        },

        "check_in_status": "have entered" if booking.checked_in_at else "havent entered yet"
    }
