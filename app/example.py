from datetime import datetime, timedelta
from core.database import add_sample_data
from services.reservation import reservation_service

add_sample_data()


def example():
    start_date_time = datetime(2023, 11, 29, 8, 0, 0)
    # array with 720 intervals
    datetimes_list = [start_date_time + timedelta(hours=i) for i in range(720)]
    reservation_service.create(room_id=1, event_id=1, intervals=datetimes_list)

    print(reservation_service.get_by_room_id(room_id=1))

    start_date_time = datetime(2022, 11, 29, 8, 0, 0)
    # array with 720 intervals
    datetimes_list = [start_date_time + timedelta(hours=i) for i in range(720)]
    reservation_service.update_by_id(reservation_id=1, room_id=2, event_id=1, intervals=datetimes_list)

    print(reservation_service.get_by_room_id(room_id=2))


example()
