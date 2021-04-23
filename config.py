from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    #class_file_manager = FileSystemManager
    path_media_file = 'media/'
    type = 'file_system'
    url_db = 'sqlite:///friss_storage.db'


@lru_cache()
def get_settings():
    return Settings()
