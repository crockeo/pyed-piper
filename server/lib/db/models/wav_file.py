from peewee import CharField
from peewee import IntegerField

from lib.db import BaseModel


class WavFile(BaseModel):
    id = IntegerField(primary_key=True)
    path = CharField()
