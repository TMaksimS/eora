"""main file для запуска приложения"""
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
            ai_response_sql = assistant.do_response(query, "sql")
            if ai_response_sql is not None:
                ai_response_sql = json.loads(ai_response_sql)
                print(f"***RAW-SQL*** {ai_response_sql['sql-query']}")
                db_response = database.some_query(ai_response_sql["sql-query"])

                LOGER.info(
                    f"Запрос: {query}. Ответ: {db_response}, {ai_response_sql['description']}"
                )
                ai_response_human = assistant.do_response(
                    f"Запрос: {query}."
                    f" Ответ: {db_response}, "
                    f"{ai_response_sql['description']}",
                    "human")
                LOGER.warning(ai_response_human)
            continue
    except KeyboardInterrupt:
        LOGER.warning("Приложение завершило работу.")
