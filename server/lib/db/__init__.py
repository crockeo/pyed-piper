from peewee import Model
from peewee import SqliteDatabase


class Database:
    DATABASE_PATH = "pyed-piper.db"

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
                cls.DATABASE_PATH, pragmas={"journal_mode": "wal"},
            )
        return cls.database_instance


class BaseModel(Model):
    class Meta:
        database = Database.get()
