from repositories.base import BaseRepository
from models.reservation import Reservation


class ReservationRepository(BaseRepository):
    model = Reservation
