from repositories.base import BaseRepository
from models.event_type import EventType


class EventTypeRepository(BaseRepository):
    model = EventType
