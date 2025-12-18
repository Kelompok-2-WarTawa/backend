import uuid
from src.models import Booking, Payment, Event, Seat, BookingStatus, PaymentStatus # Tambah Seat
from src.utils import NotFound, ValidationError
from sqlalchemy.orm import joinedload

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

        # Gunakan with_for_update() untuk mencegah race condition saat rebutan kursi
        # (Eventnya sendiri tidak perlu di-lock, kursinya yang nanti di-lock)
        event = self.session.query(Event).get(event_id)

        if not event:
            raise NotFound("Event not found")

        # LOGIKA BARU: Cari Kursi Kosong
        available_seats = self.session.query(Seat).\
            filter(Seat.event_id == event_id, Seat.booking_id == None).\
            with_for_update().\
            limit(quantity).\
            all()

        if len(available_seats) < quantity:
            # Hitung sisa real untuk pesan error
            sisa = self.session.query(Seat).filter(
                Seat.event_id == event_id, Seat.booking_id == None).count()
            
            raise ValidationError(
                "Ticket overflows (Seat penuh)",
                details={"requested": quantity, "available": sisa}
            )

        total_price = event.ticket_price * quantity
        booking_code = f"BKG-{uuid.uuid4().hex[:8].upper()}"

        # Note: Kita TIDAK lagi mengurangi event.capacity karena itu jadi patokan Total Kapasitas.
        # Ketersediaan dihitung dari count kursi yang booking_id-nya NULL.

        booking = Booking(
            customer_id=customer_id,
            event_id=event_id,
            booking_code=booking_code,
            quantity=quantity,
            total_price=total_price,
            status=BookingStatus.PENDING
        )

        self.session.add(booking)
        self.session.flush() # Flush agar booking.id terbentuk

        # Kunci kursi untuk booking ini
        for seat in available_seats:
            seat.booking_id = booking.id
            self.session.add(seat)

        return booking

    def pay_booking(self, booking_code, amount, method):
        booking = self.get_booking(booking_code)

        if booking.status != BookingStatus.PENDING:
            raise ValidationError(f"Booking Status: {booking.status.value}")

        if amount < booking.total_price:
            raise ValidationError(
                "Your money are not enough",
                details={"required": float(booking.total_price), "given": float(amount)}
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

        # Lepas Kursi (Kembalikan ke NULL)
        for seat in booking.seats:
            seat.booking_id = None
            self.session.add(seat)

        booking.status = BookingStatus.CANCELLED
        self.session.add(booking)

        return {"message": "Booking canceled, seats released"}

    def get_by_customer(self, user_id):
        # Join seat juga biar user tahu dapat kursi mana aja
        return self.session.query(Booking).\
            options(joinedload(Booking.event), joinedload(Booking.seats)).\
            filter_by(customer_id=user_id).\
            order_by(Booking.created_at.desc()).\
            all()