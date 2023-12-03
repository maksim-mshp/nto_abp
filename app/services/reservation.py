from typing import Optional
from datetime import datetime

from repositories.room import RoomRepository
from repositories.time_interval import TimeIntervalRepository
from repositories.reservation import ReservationRepository

from utils import object_as_dict


class ReservationService:
    def __init__(self):
        self.room_repository = RoomRepository()
        self.time_interval_repository = TimeIntervalRepository()
        self.reservation_repository = ReservationRepository()

    def create(
            self,
            room_id: int,
            event_id: int,
            intervals: list[datetime],
            half_reservation: bool = False
    ) -> dict:
        reservation = object_as_dict(
            self.reservation_repository.create(room_id=room_id, event_id=event_id, half_reservation=half_reservation)
        )
        self.time_interval_repository.create(reservation_id=reservation['id'], intervals=intervals)
        return reservation

    def get_by_room_id(self, room_id) -> list[dict]:
        reservations = self.reservation_repository.get_list_items_by_filter(room_id=room_id)
        results = []
        for reservation in reservations:
            result = {
                'room_id': reservation.room_id,
                'event_id': reservation.event_id,
                'intervals': [object_as_dict(interval) for interval in reservation.intervals],
            }
            results.append(result)
        return results

    def delete_by_id(self, reservation_id) -> None:
        self.reservation_repository.delete_by_id(reservation_id)

    def update_by_id(
            self,
            reservation_id: int,
            room_id: Optional[int] = None,
            event_id: Optional[int] = None,
            intervals: Optional[list[datetime]] = None,
            half_reservation: Optional[bool] = None,
    ) -> dict:
        old_reservation = self.reservation_repository.get_item_by_filter(id=reservation_id)

        if not room_id:
            room_id = old_reservation.room_id
        if not event_id:
            event_id = old_reservation.event_id
        if not half_reservation:
            half_reservation = old_reservation.half_reservation
        if not intervals:
            intervals = []
            for interval in old_reservation.intervals:
                intervals.append(object_as_dict(interval)['start_date_time'])

        self.delete_by_id(reservation_id)
        reservation = self.create(room_id, event_id, intervals, half_reservation)
        return reservation

    def get_time_intervals_by_date_and_room(self, date_time: datetime, room_id: int):
        objects_on_date = self.time_interval_repository.get_all_by_date_and_room(date_time, room_id)
        obj_as_list = [{
            'start_date_time': i.start_date_time,
            'reservation': {
                'room': i.reservation.room.name,
                'event': i.reservation.event.title,
                'half_reservation': i.reservation.half_reservation,
            }
        } for i in objects_on_date]
        return obj_as_list


reservation_service = ReservationService()
