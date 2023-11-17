from repositories.base import BaseRepository
from models.event import Event


class EventRepository(BaseRepository):
    model = Event
