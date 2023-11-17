from repositories.base import BaseRepository
from models.job_room import JobRoom


class EventTypeRepository(BaseRepository):
    model = JobRoom
