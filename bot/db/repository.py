from typing import Dict, Any

from bot.db.db_client import DbClient


class Repository:

    def __init__(self, db_client: DbClient):
        self.db_client = db_client

    def __get_one(self, table_name, fields: Dict[str, Any]):
        where_stmt = 'and '.join([f'{k} = {v}' for k, v in fields.keys()])
        select_query = f'SELECT * FROM {table_name} WHERE {where_stmt}'
        return self.db_client.fetch_one(select_query)

    def __get_one_by_fields(self, table_name, fields: Dict[str, Any]):
        with_values = {k: v for k, v in fields.items() if v is not None}
        return self.__get_one(table_name, with_values)

    def get_one_by_id(self, table_name, id_item: Dict[str, Any]):
        return self.__get_one(table_name, id_item)

    def get_one_by_entity(self, entity):
        table_name = entity.table_name()
        id_field = entity.id_field()

        if id_value := getattr(entity, id_field):
            return self.__get_one(table_name, {id_field: id_value})

        return self.__get_one_by_fields(table_name, entity.fields())

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
