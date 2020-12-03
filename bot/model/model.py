from datetime import date
from dataclasses import asdict, dataclass


@dataclass
class Entity:
    __table_name: str

    def save(self, db):
        table_name = type(self).__name__.lower() if not self.__table_name else self.__table_name
        id_field = f'{table_name}_id'

        fields = asdict(self)
        entity_id = fields[id_field]

        if entity_id is None:
            upsert_on = None
            fields.pop(id_field)
        else:
            upsert_on = [id_field]

        inserted = db.insert(table_name, fields, upsert_on=upsert_on)

        if entity_id is None:
            inserted_id = getattr(inserted.one(), id_field)
            setattr(self, id_field, inserted_id)


class User(Entity):
    __table_name = 'users'
    user_id: int
    name: str
    surname: str
    lang: str

    def __str__(self):
        return f'{self.name} {self.surname}' if self.surname else self.name


class Provider:
    __table_name = 'provider'
    provider_id: int
    name: str
    website: str

    def __str__(self):
        return f'{self.name} {self.website}' if self.website else self.name


class WOD:
    __table_name = 'wod'
    wod_id: int
    wod_day: date
    title: str
    info: str
    provider_id: int

    def __str__(self):
        return self.title
