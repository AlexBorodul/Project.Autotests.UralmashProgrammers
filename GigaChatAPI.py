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
        content="Ты программист-тестировщик, которому нужно написать автотесты для приложений банка. "
                "Твоя задача выполнить следующий алгоритм: "
                "Получить на вход файл (в формате docx или pdf) с описанием FSD. "
                "Каждый раздел FSD (начиная с 6 по предпоследний) переписывает в человеко-читаемую спецификацию. "
                "На каждую полученную спецификацию генерирует тест-кейсы. На одну спецификацию может быть "
                "от одного до нескольких тест-кейсов."
        ),
]

PROMPTS = ['Прочитай документ FSD, удели особенное внимание и запомни всё с пункта 6 (функции системы) до '
           'предпоследнего пункта документа (8) включительно. '
           'Составь и опиши 3 тест-кейса для каждой функции согласно следующему формату: Название – '
           'краткое и понятное '
           'название теста для идентификации.'
           'Идентификатор – уникальный номер или код для отслеживания кейса.'
           'Цель/Описание – краткая информация о том, что именно проверяется этим тест-кейсом.'
           'Предусловия – условия, которые должны быть выполнены перед началом выполнения тестов (например, наличие '
           'определенных данных).'
           'Шаги тестирования – пошаговые инструкции, которые необходимо выполнить для проверки функционала.'
           'Категория – к какой части системы относится данный тест-кейс (функциональность, интерфейс, '
           'безопасность и т.д.).'
           'Не используй никаких языков разметки и программирования, по типу Json или XML',

           'Используя составленные тобой тесты, составь код автотестов, используя фреймворк Cucumber']


def giga_api(task="", temp_path="", chat_with_gigachat=False):
    if chat_with_gigachat:
        prompt = task
    else:
        prompt_file = ""
        if temp_path != "":
            prompt_file = ParserToTxt(temp_path).convert()
        prompt = (
                task +
                '\n'
                + prompt_file
        )
    messages.append(HumanMessage(content=prompt))
    response = chat.invoke(messages)
    messages.append(response)
    return response
