from datetime import date

from src.schemas.booking import BookingAdd


async def test_add_hotel(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2026, month=5, day=12),
        date_to=date(year=2026, month=5, day=13),
        price=100
    )
    await db.bookings.add(booking_data)
    await db.commit()