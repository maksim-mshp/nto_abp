from repositories.base import BaseRepository
from models.job_type import JobType


class JobTypeRepository(BaseRepository):
    model = JobType
