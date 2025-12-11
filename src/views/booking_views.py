from pyramid.view import view_config
from decimal import Decimal


@view_config(route_name='bookings_create', request_method='POST', renderer='json')
def create_booking(request):
    data = request.json_body

    # Hardcode customer_id=1 for simulation
    booking = request.services.booking.create_booking(
        customer_id=1,
        event_id=int(data['event_id']),
        quantity=int(data['quantity'])
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
    data = request.json_body

    amount = Decimal(str(data['amount']))
    method = data['method']

    return request.services.booking.pay_booking(code, amount, method)


@view_config(route_name='bookings_cancel', request_method='POST', renderer='json')
def cancel_booking(request):
    code = request.matchdict['code']
    return request.services.booking.cancel_booking(code)
