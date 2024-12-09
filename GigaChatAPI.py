from docxparser import ParserToTxt
from langchain_gigachat import GigaChat
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os


load_dotenv()
chat = GigaChat(
    credentials=os.getenv("CREDIT"),
    streaming=True,
    verify_ssl_certs=False
)
messages = [
    SystemMessage(
        content="Ты программист-тестировщик, которому нужно написать автотесты для приложений банка."
        ),
]


def giga_api(temp_path):
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
    return response
