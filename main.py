from fastapi import FastAPI
from app.routers import video
from app import models
from app.database import engine

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(video.router)

