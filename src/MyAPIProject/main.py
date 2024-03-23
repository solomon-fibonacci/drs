from fastapi import FastAPI
from .router import events_router

app = FastAPI()
app.include_router(events_router, prefix="/events", tags=["Events"])