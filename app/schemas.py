from pydantic import BaseModel

class VideoBase(BaseModel):
    name: str
    description: str

class VideoCreate(VideoBase):
    pass

class VideoUpdate(VideoBase):
    pass

class Video(VideoBase):
    id: int
    path: str

    class Config:
        from_attributes = True

class ShowVideo(VideoBase):
    path:str

    class Config:
        from_attributes = True

    