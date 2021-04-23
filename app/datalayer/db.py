#
# It is set of functions/objects created
# to manage Database
#

import databases
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker

from ..config import get_settings

engine = sqlalchemy.create_engine(
    get_settings().url_db
)

Base: DeclarativeMeta = declarative_base()
database = databases.Database(get_settings().url_db)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
