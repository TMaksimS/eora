"""модуль для взаимодействия с SQLite"""
from typing import Any

import sqlite3

from scr.config import LOGER


class UoW:
    """Юнит для взаимодействия с бд"""
    #pylint: disable = too-few-public-methods
    def __init__(self):
        self._db = "eora-db"

    @LOGER.catch
    def some_query(self, sql_string: str) -> Any:
        """выполнение какого то sql запроса"""
        with sqlite3.connect(self._db) as conn:
            result = conn.execute(sql_string).fetchall()
            if len(result) <= 1:
                return result[0]
            return result
