from datetime import datetime
from enum import Enum
from typing import Dict
import json
from pydantic import BaseModel


class SortOrder(Enum):
    ASCENDING = 1
    DESCENDING = -1


def to_savable(obj: BaseModel) -> Dict:
    data = obj.model_dump()
    return data


def now() -> datetime:
    return datetime.utcnow()


def now_str() -> str:
    return datetime.utcnow().isoformat()
