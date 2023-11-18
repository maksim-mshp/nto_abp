from repositories.base import BaseRepository
from models.job import Job


class JobRepository(BaseRepository):
    model = Job
