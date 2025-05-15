from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import os
import moviepy.editor as mp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/convert-image-pdf")
async def convert_image_to_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    img = Image.open(file_path).convert("RGB")
    pdf_path = os.path.join(UPLOAD_DIR, file.filename + ".pdf")
    img.save(pdf_path, "PDF")

    return FileResponse(pdf_path, filename=os.path.basename(pdf_path))

@app.post("/convert-video-audio")
async def convert_video_to_audio(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    clip = mp.VideoFileClip(file_path)
    audio_path = file_path.rsplit(".", 1)[0] + ".mp3"
    clip.audio.write_audiofile(audio_path)

    return FileResponse(audio_path, filename=os.path.basename(audio_path))

# Additional endpoints (PDF to DOCX, etc.) would go here
