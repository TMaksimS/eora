"""main file для запуска приложения"""
import json

import openai

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
            ai_response = assistant.do_response(query)
            if ai_response is not None:
                ai_response = json.loads(ai_response)
                print(f"***RAW-SQL*** {ai_response['sql-query']}")
                db_response = database.some_query(ai_response["sql-query"])
                LOGER.info(f"{db_response}, {ai_response['description']}")
            continue
    except KeyboardInterrupt:
        LOGER.warning("Приложение завершило работу.")
