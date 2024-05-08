import io
import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from openai import OpenAI
from rembg import remove

client = OpenAI()

load_dotenv()

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"])


@app.get("/")
async def root():
    return {"Message": "api running"}


from langchain_openai import ChatOpenAI
from openai import OpenAI

service_region = "eastus"
subscription_key = os.getenv("SPEECH_KEY")
endpoint = os.getenv("AZURE_ENDPOINT")
#

llm = ChatOpenAI()


from dotenv import find_dotenv, load_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file

client = OpenAI()

llm_model = "gpt-3.5-turbo"


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


@app.post("/resume-reclamation")
async def resume_reclamation(file: UploadFile = File(...)):
    if file.content_type.startswith("audio/"):  # type: ignore
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        audio_file = open(temp_file_path, "rb")
        try:
            transcription = client.audio.transcriptions.create(
                model="whisper-1", file=audio_file, language="es"
            )

            return {"transcription": transcription.text}

        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    else:
        raise HTTPException(status_code=400, detail="Only audio files are accepted")
