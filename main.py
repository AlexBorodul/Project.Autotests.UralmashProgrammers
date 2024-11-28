from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from docxparser import ParserToTxt
from langchain_gigachat import GigaChat
from langchain_core.messages import HumanMessage, SystemMessage
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

chat = GigaChat(
    credentials="YjU2OTAwMDgtNjdlMy00ODhlLWFkMTQtYjQwN2Y1YmE1YTJhOjY1M2ZlMGZjLTk4NzEtNDEyNC1iMmFkLWYzMDM1OWFmYzhlMA==",
    streaming=True,
    verify_ssl_certs=False
)
messages = [
    SystemMessage( 
        content="Ты программист-тестировщик, которому нужно написать автотесты для приложений банка." 
        ),
]


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
        parser = ParserToTxt(temp_path)
        prompt_file = parser.convert()
        prompt = (
            'Прочитай документ FSD, учитывая все функции системы, требования к данным, болевые точки. '
            'Составь автотесты с подходом pairwise testing, используя Cucumber и напиши тестирующий код.\n'
            + prompt_file
        )
        messages.append(HumanMessage(content=prompt))
        response = chat.invoke(messages)
        messages.append(response)
        os.remove(temp_path)
        return JSONResponse(content={"message": response.content})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run(app, port=10000)

# from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import JSONResponse
# from docxparser import ParserToTxt
# from langchain.chat_models.gigachat import GigaChat
# from langchain_core.messages import HumanMessage, SystemMessage

# app = FastAPI()

# chat = GigaChat(
#     credentials="YjU2OTAwMDgtNjdlMy00ODhlLWFkMTQtYjQwN2Y1YmE1YTJhOjY1M2ZlMGZjLTk4NzEtNDEyNC1iMmFkLWYzMDM1OWFmYzhlMA==",
#     streaming=True
# )
# messages = [
#     SystemMessage(
#         content="Ты программист-тестировщик, которому нужно написать автотесты для приложений банка."
#         )
# ]

# @app.post("/upload")
# async def upload_file(file: UploadFile = File(...)):
#     try:
#         content = await file.read()
#         temp_path = f"/tmp/{file.filename}"
#         with open(temp_path, "wb") as f:
#             f.write(content)

#         parser = ParserToTxt(temp_path)
#         prompt_file = parser.convert()
#         prompt = (
#             'Прочитай документ FSD, учитывая все функции системы, требования к данным, болевые точки. '
#             'Составь автотесты с подходом pairwise testing, используя Cucumber и напиши тестирующий код.\n'
#             + prompt_file
#         )
#         messages.append(HumanMessage(content=prompt))
#         response = chat.invoke(messages)

#         return JSONResponse(content={"message": response.content})
#     except Exception as e:
#         return JSONResponse(content={"error": str(e)}, status_code=500)