from sqlalchemy.orm import Session
from app import models, schemas


def create_video(db: Session, video: schemas.VideoCreate, path: str):
    db_video = models.Video(name=video.name, description=video.description, path=path)
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video

def get_video_by_id(db: Session, video_id: int):
    return db.query(models.Video).filter(models.Video.id == video_id).first()

def get_videos_by_name(db: Session, name: str):
    return db.query(models.Video).filter(models.Video.name.contains(name)).all()

def delete_video(db: Session, video_id: int):
    db_video = get_video_by_id(db, video_id)
    if db_video:
        db.delete(db_video)
        db.commit()
        return True
    return False

def update_video(db: Session, video_id: int, video: schemas.VideoUpdate):
    db_video = get_video_by_id(db, video_id)
    if db_video:
        db_video.name = video.name
        db_video.description = video.description
        db.commit()
        db.refresh(db_video)
        return db_video
    return None