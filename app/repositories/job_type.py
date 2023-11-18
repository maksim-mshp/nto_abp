from repositories.base import BaseRepository
from models.job_type import JobType


class EventTypeRepository(BaseRepository):
    model = JobType
