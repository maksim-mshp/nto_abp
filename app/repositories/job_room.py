from repositories.base import BaseRepository
from models.job_room import JobRoom


class JobRoomRepository(BaseRepository):
    model = JobRoom
