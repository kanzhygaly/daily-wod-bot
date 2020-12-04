from typing import Dict, Any

from bot.db.db_client import DBClient


class Repository:

    def __init__(self, db_client: DBClient):
        self.db_client = db_client

    def get_one(self, table_name, fields: Dict[str, Any]):
        where_stmt = 'and '.join([f'{k} = {v}' for k, v in fields.keys()])
        select_query = f'SELECT * FROM {table_name} WHERE {where_stmt}'
        return self.db_client.fetch_one(select_query)

    def get_one_by_id(self, table_name, id_item: Dict[str, Any]):
        return self.get_one(table_name, id_item)

    def get_one_by_other(self, table_name, fields: Dict[str, Any], excluded_field: str):
        fields.pop(excluded_field)
        return self.get_one(table_name, fields)

    def insert(self, table_name, fields: Dict[str, Any]):
        columns = ', '.join(list(fields.keys()))
        placeholders = ', '.join(['%s' for i in range(len(fields))])

        insert_query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'

        self.db_client.execute(query=insert_query, args=tuple(fields.values()))

    def update(self, table_name, fields: Dict[str, Any], id_field: str):
        id_value = fields.pop(id_field)

        set_stmt = ', '.join([f'{k} = %s' for k in fields.keys()])
        where_stmt = f'{id_field} = %s'

        update_query = f'UPDATE {table_name} SET {set_stmt} WHERE {where_stmt}'

        values = list(fields.values())
        values.append(id_value)

        self.db_client.execute(query=update_query, args=tuple(values))
