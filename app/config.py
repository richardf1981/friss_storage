import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    path_media_file = "{}".format(os.getenv("MEDIA_LOCATION", "app/media/"))
    type = 'file_system'
    url_db = 'sqlite:///{}'.format(
        os.getenv("DB_FILE_LOCATION", "app/data/friss_storage.db"))
    logger_middleware_on = True


@lru_cache()
def get_settings():
    return Settings()
