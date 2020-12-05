import uuid
from datetime import date
from dataclasses import asdict, dataclass
from typing import Tuple
from uuid import UUID

from bot.db.repository import Repository


@dataclass
class Entity:

    def save(self, repo: Repository):
        update = False
        table_name = self.table_name()
        id_field = self.id_field()

        if id_value := getattr(self, id_field):
            record = repo.get_one_by_id(table_name, {id_field: id_value})
            update = True if record else False

        if not id_value and type(id_value) is uuid.UUID:
            id_value = uuid.uuid4()
            setattr(self, id_field, id_value)

        fields = self.fields()

        if update:
            repo.update(table_name, fields, id_field)
        else:
            repo.insert(table_name, fields)

    def table_name(self):
        return type(self).__name__.lower()

    def id_field(self):
        return f'{self.table_name()}_id'

    def fields(self):
        return asdict(self)

    def __parse_from_record(self, record: Tuple):
        field_keys = list(self.fields())
        field_count = len(field_keys)

        if field_count == len(record):
            for i in range(field_count):
                setattr(self, field_keys[i], record[i])

    @classmethod
    def from_record(cls, record: Tuple):
        entity = cls()
        entity.__parse_from_record(record)
        return entity


@dataclass
class Users(Entity):
    users_id: int = None
    name: str = None
    surname: str = None
    lang: str = None

    def __str__(self):
        return f'{self.name} {self.surname}' if self.surname else self.name


@dataclass
class Provider(Entity):
    provider_id: UUID = None
    name: str = None
    website: str = None

    def __str__(self):
        return f'{self.name} {self.website}' if self.website else self.name


@dataclass
class WOD(Entity):
    wod_id: UUID = None
    wod_day: date = None
    title: str = None
    content: str = None
    provider_id: UUID = None

    def __str__(self):
        return self.title
