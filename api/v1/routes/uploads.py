import os
from moviepy.editor import VideoFileClip
import uuid
from fastapi import (Depends, 
                     APIRouter, 
                     UploadFile, 
                     Request, 
                     status, 
                     File,
                     Query, 
                     HTTPException
                     )
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from api.utils.success_response import success_response
from api.v1.services.user import user_service

# Define the temporary directories for uploads
UPLOAD_DIR = "uploads/original"
CHUNKS_DIR = "uploads/chunks"

# Ensure folders exist

try:
    if not os.makedirs(UPLOAD_DIR and CHUNKS_DIR, exist_ok=True):
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        os.makedirs(UPLOAD_DIR,  exist_ok=True)
except Exception as e:
    print(f"Error creating media directory: {e}")
    pass 


upload_router = APIRouter(prefix="/upload", tags=["Uploads"])


@upload_router.post("/upload/")
async def upload_video(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.endswith(('.mp4', '.mov', '.avi', '.mkv')):
        raise HTTPException(status_code=400, detail="Unsupported file format")

    # Save the uploaded file
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    # Chunk the video
    chunk_paths = chunk_video(file_path, CHUNKS_DIR)

    return JSONResponse(content={
        "message": "Video uploaded and chunked successfully.",
        "chunks": chunk_paths
    })

def chunk_video(video_path: str, output_dir: str, chunk_length: int = 5):
    video = VideoFileClip(video_path)
    duration = int(video.duration)
    print(type(video))
    print(video.duration)
    base_filename = os.path.splitext(os.path.basename(video_path))[0]

    chunk_paths = []

    for start in range(0, duration, chunk_length):
        end = min(start + chunk_length, duration)
        chunk_filename = f"{base_filename}_chunk_{start}_{end}.mp4"
        print(f"Chunking video: {chunk_filename} from {start} to {end}")
        chunk_path = os.path.join(output_dir, chunk_filename)

        video.subclip(start, end).write_videofile(chunk_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)
        chunk_paths.append(chunk_path)

    return chunk_paths