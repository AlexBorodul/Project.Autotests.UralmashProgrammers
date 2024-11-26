from langchain.chat_models.gigachat import GigaChat
from langchain_core.messages import HumanMessage, SystemMessage
from docxparser import ParserToTxt

chat = GigaChat(credentials="YjU2OTAwMDgtNjdlMy00ODhlLWFkMTQtYjQwN2Y1YmE1YTJhOjY1M2ZlMGZjLTk4NzEtNDEyNC1iMmFkLWYzMDM1OWFmYzhlMA==", streaming=True)
messages = [
    SystemMessage(
        content="Ты программист-тестировщик, которому нужно написать автотесты для приложений банка."
    )
]
# prompt_file = ParserToTxt("test_fsd.docx").convert()
# print(PROMPT)

while True:
    user_input = input("Введите путь до файла: ")
    if user_input == "пока": break
    prompt_file = ParserToTxt(user_input).convert()
    PROMPT = ('Прочитай документ FSD, учитывая все функции системы, требования к данным, болевые точки. '
              'Составь автотесты с подходом pairwise testing, используя Cucumber и напиши тестирующий код.' + '\n' +
              prompt_file)
    messages.append(HumanMessage(content=PROMPT + '\n' + prompt_file))
    res = chat.invoke(messages)
    messages.append(res)
    print("GigaChat: ", res.content)
