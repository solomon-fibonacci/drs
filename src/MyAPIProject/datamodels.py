from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class EventType(Enum):
    CONFERENCE = "conference"
    MEETUP = "meetup"
    WORKSHOP = "workshop"

class EventStatus(Enum):
    SCHEDULED = "scheduled"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class EventModel(BaseModel):
    id: str
    name: str
    description: str
    event_type: EventType
    start_time: datetime
    end_time: datetime
    location: str
    status: EventStatus = Field(default=EventStatus.SCHEDULED)
    attendees: List[str] = Field(default=[])