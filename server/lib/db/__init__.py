from peewee import Model
from peewee import SqliteDatabase
from playhouse.shortcuts import dict_to_model
from playhouse.shortcuts import model_to_dict
import json

from lib.common import config


class Database:
    database_instance = None

    @classmethod
    def get(cls) -> SqliteDatabase:
        """
        Singleton pattern for peewee database instance. Constructs a
        SqliteDatabase if it does not exist prior. Returns the SqliteDatabase
        once constructed.
        """
        if cls.database_instance is None:
            cls.database_instance = SqliteDatabase(
                config.DATABASE_PATH, pragmas={"journal_mode": "wal"},
            )
        return cls.database_instance


class BaseModel(Model):
    class Meta:
        database = Database.get()

    def to_json(self) -> str:
        """
        Serializes the child of this BaseModel to JSON.
        """
        return json.dumps(model_to_dict(self))
