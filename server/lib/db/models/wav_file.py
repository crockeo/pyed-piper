from peewee import CharField
from peewee import UUIDField

from lib.db import BaseModel


class WavFile(BaseModel):
    id = UUIDField(primary_key=True)
    path = CharField()
    name = CharField()
