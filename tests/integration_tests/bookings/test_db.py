from datetime import date

from src.schemas.booking import BookingAdd


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2026, month=5, day=12),
        date_to=date(year=2026, month=5, day=13),
        price=100,
    )
    new_booking = await db.bookings.add(booking_data)
    await db.commit()

    # получить эту бронь и убедиться что она есть
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.id == new_booking.id
    assert booking.room_id == new_booking.room_id
    assert booking.user_id == new_booking.user_id

    # обновить бронь
    update_booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2026, month=5, day=10),
        date_to=date(year=2026, month=5, day=11),
        price=1000,
    )

    await db.bookings.edit(update_booking_data, id=new_booking.id)
    updated_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert updated_booking
    await db.commit()
    assert updated_booking.id == new_booking.id
    assert updated_booking.date_to == update_booking_data.date_to
    assert updated_booking.date_from == update_booking_data.date_from

    # удалить бронь
    await db.bookings.delete(id=new_booking.id)
    await db.commit()
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert not booking
