import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    path_media_file = "{}".format(os.getenv("MEDIA_LOCATION", "app/media/"))
    type = 'file_system'

    url_db = '{}'.format(
        os.getenv("CONNECTION_STRING",
                  "mysql://root:@127.0.0.1/friss_storage?charset=utf8mb4"))

    logger_middleware_on = True


@lru_cache()
def get_settings():
    return Settings()
