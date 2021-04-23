from fastapi_users import models
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase

from app.datalayer import db


class User(models.BaseUser):
    pass


class UserDB(User, models.BaseUserDB):
    pass


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserTable(db.Base, SQLAlchemyBaseUserTable):
    pass


users = UserTable.__table__
user_db = SQLAlchemyUserDatabase(UserDB, db.database, users)
