from langchain.chat_models.gigachat import GigaChat
from langchain_core.messages import HumanMessage, SystemMessage
import docxparser

chat = GigaChat(credentials="YjU2OTAwMDgtNjdlMy00ODhlLWFkMTQtYjQwN2Y1YmE1YTJhOjY1M2ZlMGZjLTk4NzEtNDEyNC1iMmFkLWYzMDM1OWFmYzhlMA==", streaming=True)
messages = [
    SystemMessage(
        content="Ты программист-тестировщик, которому нужно написать автотесты для приложений банка."
    )
]

while True:
    user_input = input("Пользователь: ")
    if user_input == "пока": break
    messages.append(HumanMessage(content=user_input))
    res = chat.invoke(messages)
    messages.append(res)
    print("GigaChat: ", res.content)
