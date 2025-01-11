from pathlib import Path
from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from pdf2docx_converter import pdf_to_docx
import os
from GigaChatAPI import giga_api, PROMPTS
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="project/static"), name="static")
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "tmp"
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/")
async def main():
    return FileResponse("index.html")


@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    try:
        responses = []
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in [".pdf", ".docx"]:
            raise HTTPException(status_code=400, detail="Файл должен быть формата PDF или DOCX")
        temp_path = UPLOAD_DIR / file.filename
        with open(temp_path, "wb") as temp_file:
            temp_file.write(file.file.read())
        if file_ext == ".pdf":
            docx_path = temp_path.with_suffix(".docx")
            try:
                pdf_to_docx(str(temp_path), str(docx_path))
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Ошибка конвертации PDF: {str(e)}")
            temp_path.unlink()
            temp_path = docx_path
        for i in range(len(PROMPTS)):
            response = giga_api(PROMPTS[i], temp_path)
            responses.append(response.content)
        temp_path.unlink()
        return JSONResponse(content={"message": responses})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/chat")
async def chat_with_gigachat(request: Request):
    try:
        data = await request.json()
        user_message = data.get("message")
        if not user_message:
            return JSONResponse(content={"error": "Сообщение не может быть пустым."}, status_code=400)
        response = giga_api(user_message, chat_with_gigachat=True)
        return JSONResponse(content={"reply": response.content})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run(app, port=10000)
