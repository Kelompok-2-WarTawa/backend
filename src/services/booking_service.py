import uuid
from src.models import Booking, Payment, Event, BookingStatus, PaymentStatus
from src.utils import NotFound, ValidationError


class BookingService:
    def __init__(self, session):
        self.session = session

    def get_booking(self, booking_code):
        booking = self.session.query(Booking).\
            filter_by(booking_code=booking_code).first()

        if not booking:
            raise NotFound(f"Booking code {booking_code} not found")
        return booking

    def create_booking(self, customer_id, event_id, quantity):
        if quantity <= 0:
            raise ValidationError("ticket availability need to be more than 0")

        event = self.session.query(Event).with_for_update().get(event_id)

        if not event:
            raise NotFound("Event not found")

        if event.capacity < quantity:
            raise ValidationError(
                "Ticket overflows (lol)",
                details={"requested": quantity, "available": event.capacity}
            )

        total_price = event.ticket_price * quantity
        booking_code = f"BKG-{uuid.uuid4().hex[:8].upper()}"

        event.capacity -= quantity

        booking = Booking(
            customer_id=customer_id,
            event_id=event_id,
            booking_code=booking_code,
            quantity=quantity,
            total_price=total_price,
            status=BookingStatus.PENDING
        )

        self.session.add(booking)
        self.session.flush()
        return booking

    def pay_booking(self, booking_code, amount, method):
        booking = self.get_booking(booking_code)

        if booking.status != BookingStatus.PENDING:
            raise ValidationError(f"Booking Status: {
                                  booking.status.value}")

        if amount < booking.total_price:
            raise ValidationError(
                "Your money are not enough",
                details={"required": float(
                    booking.total_price), "given": float(amount)}
            )

        payment = Payment(
            booking_id=booking.id,
            amount=amount,
            method=method,
            status=PaymentStatus.SUCCESS
        )

        booking.status = BookingStatus.CONFIRMED

        self.session.add(payment)
        self.session.flush()
        return payment

    def cancel_booking(self, booking_code):
        booking = self.get_booking(booking_code)

        if booking.status == BookingStatus.CANCELLED:
            raise ValidationError("Booking been canceled previously")

        if booking.status == BookingStatus.CONFIRMED:
            pass

        event = self.session.query(Event).get(booking.event_id)
        event.capacity += booking.quantity

        booking.status = BookingStatus.CANCELLED
        self.session.add(booking)

        return {"message": "Booking canceled, ticket quota been returned"}
