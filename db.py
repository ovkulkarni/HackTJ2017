from peewee import SqliteDatabase, PostgresqlDatabase, Model
import settings

db = PostgresqlDatabase(settings.DATABASE["NAME"],
        user=settings.DATABASE["USER"],
        password=settings.DATABASE["PASSWORD"],
        host=settings.DATABASE["HOST"])

if settings.DEBUG:
    db = SqliteDatabase("database.db")

class BaseModel(Model):
    class Meta:
        if DEBUG:
            database = db
