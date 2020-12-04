from datetime import date
from dataclasses import asdict, dataclass
from typing import Tuple

from bot.db.repository import Repository


@dataclass
class Entity:

    def save(self, repo: Repository, update: bool = False):
        id_field = f'{self.table_name()}_id'
        table_name = self.table_name()
        fields = self.fields()

        if update:
            repo.update(table_name, fields, id_field)
        else:
            repo.insert(table_name, fields)
            if not getattr(self, id_field):
                record = repo.get_one_by_other(table_name, fields, id_field)
                self.__parse_from_record(record)

    def table_name(self):
        return type(self).__name__.lower()

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
class Provider:
    provider_id: int = None
    name: str = None
    website: str = None

    def __str__(self):
        return f'{self.name} {self.website}' if self.website else self.name


@dataclass
class WOD:
    wod_id: int = None
    wod_day: date = None
    title: str = None
    info: str = None
    provider_id: int = None

    def __str__(self):
        return self.title
