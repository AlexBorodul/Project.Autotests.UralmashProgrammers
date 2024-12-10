from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from GigaChatAPI import giga_api
from fastapi.staticfiles import StaticFiles
from GigaChatAPI import PROMPTS
import uvicorn
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
responses = []


@app.get("/")
async def main():
    return FileResponse("index.html")


@app.post("/")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        temp_path = f"tmp/{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(content)
        for i in range(len(PROMPTS)):
            response = giga_api(PROMPTS[i], temp_path)
            responses.append(response.content)
        return JSONResponse(content={"message": responses})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run(app, port=10000)
