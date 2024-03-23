template = """
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Import routers from your modules. Example:
from .router import books_router

all_origins = ["*"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=all_origins,
    allow_methods=all_origins,
    allow_headers=all_origins,
    max_age=600,
)


# Mount router.
# Replace 'books_router' with the actual router name.
app.include_router(books_router, prefix="/books", tags=["books"])
# Add other routes or router mounts as needed

"""
