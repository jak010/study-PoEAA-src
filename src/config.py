from __future__ import annotations

from functools import cached_property

import pymysql
from pymysql.cursors import Cursor, DictCursor
from pymysql.connections import Connection

host = "127.0.0.1"
port = 9902
user = "root"
password = "1234"
db = "pofeaa"


def get_connection() -> Connection:
    return pymysql.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        db=db,
        cursorclass=DictCursor
    )


class DataBase:

    @cached_property
    def connection(self) -> Connection:
        return get_connection()

    @cached_property
    def _cursor(self) -> Cursor:
        return self.connection.cursor()

    def execute(self, sql, params=None):
        r = self._cursor.execute(sql, params)
        print("[LOGGING]", self._cursor._executed)
        return r

    def fetchone(self):
        return self._cursor.fetchone()

    def fetchall(self):
        return self._cursor.fetchall()

    def close(self):
        self._cursor.close()
        self.connection.close()

    def commit(self):
        return self.connection.commit()

    def rollback(self):
        return self.connection.rollback()
