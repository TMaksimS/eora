import json

from scr.ai.assistant import AssistantOpenAI
from scr.config import LOGER
from scr.database import UoW

if __name__ == "__main__":
    assistant = AssistantOpenAI()
    database = UoW()
    LOGER.warning("Приложение запустилось.")
    try:
        while True:
            query = input("Введите свой запрос: ")
            ai_response: dict = json.loads(assistant.do_response(query))
            print(f"***RAW-SQL*** {ai_response['sql-query']}")
            db_response = database.some_query(ai_response["sql-query"])
            LOGER.info(f"{db_response}, {ai_response['description']}")
    except KeyboardInterrupt:
        LOGER.warning("Приложение завершило работу.")