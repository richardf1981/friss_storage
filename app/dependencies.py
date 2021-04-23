import os

from fastapi import Request
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from loguru import logger

from .datalayer.models_jwtuser import user_db, User, UserCreate, UserUpdate, UserDB
from .services.filesystem_managers import FileSystemManager

SECRET_JWT = os.getenv("SECRET_JWT", "KzyYjvjQJ8)~^w`Bs{8#</[m=V>R-[xd")
NAME_JWT = os.getenv("NAME_JWT", "fwB<6;3zDPVZ.LCm!'^T,-?q%Ux=^:yQ")
SECONDS_LIFE_TIME_JWT = int(os.getenv("SECONDS_LIFE_TIME_JWT", 36000))

auth_backends = []

jwt_authentication = JWTAuthentication(
    secret=SECRET_JWT,
    lifetime_seconds=SECONDS_LIFE_TIME_JWT,
    name=NAME_JWT
)

auth_backends.append(jwt_authentication)

fastapi_users = FastAPIUsers(
    user_db,
    auth_backends,
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

# by changing this class is possible loads any other file manager
class_file_manager = FileSystemManager


async def logging_dependency(request: Request):
    logger.debug(f"{request.method} {request.url}")
    logger.debug("Params:")
    for name, value in request.path_params.items():
        logger.debug(f"\t{name}: {value}")
    logger.debug("Headers:")
    for name, value in request.headers.items():
        logger.debug(f"\t{name}: {value}")
