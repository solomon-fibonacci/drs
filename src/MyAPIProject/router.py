from fastapi import APIRouter, HTTPException, status
from typing import List
from models import EventModel

router = APIRouter()

@router.get("/events", response_model=List[EventModel], status_code=status.HTTP_200_OK)
async def read_events():
    # Implementation goes here
    pass

@router.post("/events", response_model=EventModel, status_code=status.HTTP_201_CREATED)
async def create_event(event: EventModel):
    # Implementation goes here
    pass

@router.get("/events/{event_id}", response_model=EventModel, status_code=status.HTTP_200_OK)
async def read_event(event_id: str):
    # Implementation goes here
    pass

@router.put("/events/{event_id}", response_model=EventModel, status_code=status.HTTP_200_OK)
async def update_event(event_id: str, event: EventModel):
    # Implementation goes here
    pass

@router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(event_id: str):
    # Implementation goes here
    pass