from datetime import datetime, timedelta

import sqlalchemy

from core.database import add_sample_data, session_maker
from models.time_interval import TimeInterval
from services.event import event_service
from utils import object_as_dict, CATEGORIES

add_sample_data()


def example():
    # create
    # start_date_time = datetime(2023, 11, 29, 8, 0, 0)
    # datetimes_list = [start_date_time + timedelta(hours=i) for i in range(720)]
    # print(datetimes_list)
    # reservation_service.create(room_id=1, event_id=1, intervals=datetimes_list)
    #
    # print(reservation_service.get_by_room_id(room_id=1))
    #
    # # update
    # start_date_time = datetime(2022, 11, 29, 8, 0, 0)
    # datetimes_list = [start_date_time + timedelta(hours=i) for i in range(720)]
    # reservation_service.update_by_id(reservation_id=1, room_id=2, event_id=1, intervals=datetimes_list)
    #
    # print(reservation_service.get_by_room_id(room_id=2))
    #
    # # create half
    # start_date_time = datetime(2023, 12, 7, 9, 0, 0)
    # datetimes_list = [start_date_time + timedelta(hours=i) for i in range(3)]
    # reservation_service.create(room_id=1, event_id=1, intervals=datetimes_list, half_reservation=False)
    #
    # obj_as_list = reservation_service.get_time_intervals_by_date_and_room(datetime(2023, 12, 1), 1)
    # print(obj_as_list)

    club = event_service.create_club_type('кружок')
    teacher = event_service.create_teacher('КАКОЙ - ТО ЧЕЛ')
    event_service.create_event('title', datetime(2023, 12, 1), category=CATEGORIES[0], club_type=club['name'], teacher=teacher['name'])


example()
