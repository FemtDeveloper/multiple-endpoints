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


from langchain_openai import ChatOpenAI
from openai import OpenAI

#

llm = ChatOpenAI()


from dotenv import find_dotenv, load_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file

client = OpenAI()

llm_model = "gpt-3.5-turbo"


# get_completion("What is 1+1?")


customer_email = """
Arrr, I be fuming that me blender lid \
flew off and splattered me kitchen walls \
with smoothie! And to make matters worse,\
the warranty don't cover the cost of \
cleaning up me kitchen. I need yer help \
right now, matey!
"""
style = """Colombian Paisa in a angry and disrespectful tone"""

prompt = f"""Translate the text \
that is delimited by triple backticks
into a style that is {style}.
text: ```{customer_email}```
"""
# response = get_completion(prompt)


# print(response)


@app.get("/chatgpt-response")
async def get_completion(prompt: str, model=llm_model):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model, messages=messages, temperature=0  # type: ignore
    )  # type:ignore
    print(response.choices[0].message.content)


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
