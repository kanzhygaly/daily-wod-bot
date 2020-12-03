import psycopg2
from psycopg2 import pool


class DBClient:

    def __init__(self):
        try:
            min_conn = 1
            max_conn = 20

            self.__connection_pool = psycopg2.pool.ThreadedConnectionPool(min_conn, max_conn,
                                                                          user='<user>',
                                                                          password='<password>',
                                                                          host='<host>',
                                                                          port='<port>',
                                                                          database='<db_name>')
        except (Exception, psycopg2.Error) as error:
            print('Error while connecting to DB', error)

    def quit(self):
        if self.__connection:
            self.__connection_pool.closeall()

    def fetch_one(self, query: str):
        self.__open_connection()

        self.__cursor.execute(query)
        record = self.__cursor.fetchone()

        self.__close_connection()
        return record

    def fetch_many(self, query: str, size: int):
        self.__open_connection()

        self.__cursor.execute(query)
        records = self.__cursor.fetchmany(size)

        self.__close_connection()
        return records

    def fetch_all(self, query: str):
        self.__open_connection()

        self.__cursor.execute(query)
        records = self.__cursor.fetchall()

        self.__close_connection()
        return records

    def execute(self, statement: str):
        self.__open_connection()

        self.__cursor.execute(statement)
        self.__connection.commit()

        self.__close_connection()

    def __open_connection(self):
        self.__connection = self.__connection_pool.getconn()
        self.__cursor = self.__connection.cursor()

    def __close_connection(self):
        if self.__connection:
            self.__cursor.close()
            self.__connection_pool.putconn(self.__connection)