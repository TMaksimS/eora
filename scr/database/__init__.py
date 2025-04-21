from typing import Any

import sqlite3

from scr.config import LOGER


class UoW:
    def __init__(self):
        self._db = "eora-db"

    @LOGER.catch
    def some_query(self, sql_string: str) -> Any:
        with sqlite3.connect(self._db) as conn:
            result = conn.execute(sql_string).fetchall()
            if len(result) <= 1:
                return result[0]
            return result
