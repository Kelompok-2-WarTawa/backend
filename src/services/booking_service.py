import uuid
from datetime import datetime
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from src.models import (Booking, Payment, Event, Seat, TicketPhase,
                        BookingStatus, PaymentStatus, EventStatus, User)
from src.utils import NotFound, ValidationError
from src.config.settings import booking_settings


class BookingService:
    def __init__(self, session):
        self.session = session

    def get_booking(self, booking_code):
        booking = self.session.query(Booking).\
            options(
                joinedload(Booking.event),
                joinedload(Booking.phase),
                joinedload(Booking.seats)
        ).\
            filter_by(booking_code=booking_code).first()

        if not booking:
            raise NotFound(f"Booking code {booking_code} not found")

        return booking

    def create_booking(self, customer_id, event_id, phase_id, quantity, seat_ids):
        if quantity <= 0:
            raise ValidationError("Quantity must be > 0")

        if len(seat_ids) != quantity:
            raise ValidationError(f"Quantity mismatch: You ordered {
                                  quantity} tickets but selected {len(seat_ids)} seats.")

        event = self.session.query(Event).get(event_id)
        if not event:
            raise NotFound("Event not found")

        if event.status != EventStatus.PUBLISHED:
            raise ValidationError("Event not published yet")

        if event.date < datetime.now():
            raise ValidationError("Event has ended")

        phase = self.session.query(TicketPhase).get(phase_id)
        if not phase or phase.event_id != event_id:
            raise NotFound("Ticket phase invalid")

        now = datetime.now()
        if now < phase.start_date:
            raise ValidationError(
                f"Sales for {phase.name} haven't started yet")
        if now > phase.end_date:
            raise ValidationError(f"Sales for {phase.name} have ended")

        sold_in_phase = self.session.query(func.sum(Booking.quantity))\
            .filter(Booking.phase_id == phase_id)\
            .filter(Booking.status != BookingStatus.CANCELLED)\
            .scalar() or 0

        if sold_in_phase + quantity > phase.quota:
            remaining = phase.quota - sold_in_phase
            raise ValidationError(
                f"Sold out for {phase.name}! Remaining: {remaining}")

        user = self.session.query(User).get(customer_id)
        if not user.nik:
            raise ValidationError("Please fulfill your NIK first in profile")

        bought_count = self.session.query(func.sum(Booking.quantity))\
            .filter(Booking.customer_id == customer_id, Booking.event_id == event_id)\
            .filter(Booking.status != BookingStatus.CANCELLED)\
            .scalar() or 0

        limit = booking_settings.MAX_TICKETS_PER_USER
        if bought_count + quantity > limit:
            raise ValidationError(
                f"Max {limit} tickets per person. You have {bought_count}")

        selected_seats = self.session.query(Seat).\
            filter(Seat.id.in_(seat_ids)).\
            filter(Seat.event_id == event_id).\
            with_for_update().\
            all()

        if len(selected_seats) != len(seat_ids):
            raise NotFound(
                "Some selected seat IDs are invalid or belong to another event")

        taken_seats = []
        for seat in selected_seats:
            if seat.booking_id is not None:
                taken_seats.append(seat.seat_label)

        if taken_seats:
            raise ValidationError(
                f"Seats {', '.join(taken_seats)} are already booked by someone else.")

        total_price = phase.price * quantity
        booking_code = f"BKG-{uuid.uuid4().hex[:8].upper()}"

        booking = Booking(
            customer_id=customer_id,
            event_id=event_id,
            phase_id=phase.id,
            booking_code=booking_code,
            quantity=quantity,
            total_price=total_price,
            status=BookingStatus.PENDING
        )

        self.session.add(booking)
        self.session.flush()

        for seat in selected_seats:
            seat.booking_id = booking.id
            self.session.add(seat)

        return booking

    def pay_booking(self, booking_code, amount, method):
        booking = self.get_booking(booking_code)

        if booking.status != BookingStatus.PENDING:
            raise ValidationError(f"Booking Status: {booking.status.value}")

        if amount < booking.total_price:
            raise ValidationError(
                "Insufficient payment amount",
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
            raise ValidationError("Booking already canceled")

        for seat in booking.seats:
            seat.booking_id = None
            self.session.add(seat)

        booking.status = BookingStatus.CANCELLED
        self.session.add(booking)

        return {"message": "Booking canceled, seats released"}

    def get_by_customer(self, user_id):
        return self.session.query(Booking).\
            options(joinedload(Booking.event), joinedload(Booking.seats), joinedload(Booking.phase)).\
            filter_by(customer_id=user_id).\
            order_by(Booking.created_at.desc()).\
            all()

    def check_in_ticket(self, booking_code):
        booking = self.get_booking(booking_code)
        if booking.status != BookingStatus.CONFIRMED:
            raise ValidationError("Ticket not paid/confirmed")
        if booking.checked_in_at:
            raise ValidationError(f"Ticket already used at {
                                  booking.checked_in_at}")

        booking.checked_in_at = datetime.now()
        return {"message": "Check-in Succeded", "guest": booking.customer.name}
