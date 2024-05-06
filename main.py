import io
import os

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from rembg import remove

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"])


@app.get("/")
async def root():
    return {"Message": "api running"}


@app.post("/images/upload")
async def remove_bg(file: UploadFile = File(...)):
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)

    file_data = await file.read()

    output_bytes = remove(file_data)

    buffer = io.BytesIO(output_bytes)  # type: ignore
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="image/png",
        headers={"Content-Disposition": "attachment; filename=removed_image.png"},
    )
