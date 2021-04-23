#
# Models which represents management of
# file
#

import datetime
import uuid

from datalayer.db import Base
from fastapi_users.db.sqlalchemy import GUID
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey


class FileManagerDataAccess(Base):
    __tablename__ = "file_manager"
    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    file_name = Column(String, unique=True)
    mime_type = Column(String)
    user_id_created = Column(GUID, ForeignKey('user.id'))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    file_size = Column(Integer)


class FileManagerHistory(Base):
    __tablename__ = "file_history"
    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    id_file = Column(GUID, ForeignKey('file_manager.id'))
    updated_date = Column(DateTime, default=datetime.datetime.utcnow)
    user_id_updated = Column(GUID, ForeignKey('user.id'))
    file_size = Column(Integer)
    type_access = Column(String)