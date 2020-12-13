from typing import Tuple

import psycopg2
from psycopg2 import pool

from bot.dto.dto import DbCredentials


class DbClient:

    def __init__(self, credentials: DbCredentials):
        try:
            min_conn = 1
            max_conn = 20

            self.__connection_pool = psycopg2.pool.ThreadedConnectionPool(min_conn, max_conn,
                                                                          user=credentials.user,
                                                                          password=credentials.password,
                                                                          host=credentials.host,
                                                                          port=credentials.port,
                                                                          database=credentials.database)
        except (Exception, psycopg2.Error) as error:
            print('Error while connecting to DB', error)

    def quit(self):
        if self.__connection:
            self.__connection_pool.closeall()

    def fetch_one(self, query: str, args: Tuple):
        self.__open_connection()

        self.__cursor.execute(query, args)
        record = self.__cursor.fetchone()

        self.__close_connection()
        return record

    def fetch_many(self, query: str, args: Tuple, size: int):
        self.__open_connection()

        self.__cursor.execute(query, args)
        records = self.__cursor.fetchmany(size)

        self.__close_connection()
        return records

    def fetch_all(self, query: str, args: Tuple):
        self.__open_connection()

        self.__cursor.execute(query, args)
        records = self.__cursor.fetchall()

        self.__close_connection()
        return records

    def execute(self, query: str, args: Tuple = None):
        self.__open_connection()

        if args:
            self.__cursor.execute(query, args)
        else:
            self.__cursor.execute(query)

        self.__connection.commit()
        self.__close_connection()

    def __open_connection(self):
        self.__connection = self.__connection_pool.getconn()
        self.__cursor = self.__connection.cursor()

    def __close_connection(self):
        if self.__connection:
            self.__cursor.close()
            self.__connection_pool.putconn(self.__connection)
