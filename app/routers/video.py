from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import os
from app import crud, models, schemas, database

router = APIRouter(
    prefix="/videos",
    tags=["Videos"],
)

VIDEO_DIR = "videos"
if not os.path.exists(VIDEO_DIR):
    os.makedirs(VIDEO_DIR)

ALLOWED_VIDEO_EXTENSIONS = [".mp4"]

get_db = database.get_db


# Upload a new video
@router.post("/", response_model=schemas.Video)
def upload_video(name: str, description: str, file: UploadFile = File(...), db: Session = Depends(get_db)):

    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in ALLOWED_VIDEO_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file format: {file_extension}. Only .mp4 files are allowed."
        )
    file_path = os.path.join(VIDEO_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())
    
    video = crud.create_video(db, video=schemas.VideoCreate(name=name, description=description), path=file_path)
    return video

# Search videos by name
@router.get("/", response_model=list[schemas.ShowVideo])
def search_videos(name: str, db: Session = Depends(get_db)):
    videos = crud.get_videos_by_name(db, name=name)
    if not videos:
        raise HTTPException(status_code=404, detail="Video not found")
    return videos

# Delete video by ID
@router.delete("/{video_id}", response_model=bool)
def delete_video(video_id: int, db: Session = Depends(get_db)):
    result = crud.delete_video(db, video_id=video_id)
    if not result:
        raise HTTPException(status_code=404, detail="Video not found")
    return True

# Update video details by ID
@router.put("/{video_id}", response_model=schemas.Video)
def update_video(video_id: int, video: schemas.VideoUpdate, db: Session = Depends(get_db)):
    db_video = crud.update_video(db, video_id=video_id, video=video)
    if not db_video:
        raise HTTPException(status_code=404, detail="Video not found")
    return db_video