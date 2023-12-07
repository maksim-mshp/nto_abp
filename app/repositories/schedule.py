from repositories.base import BaseRepository
from models.schedule import Schedule


class ScheduleRepository(BaseRepository):
    model = Schedule
