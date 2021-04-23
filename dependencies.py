import os

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from datalayer.models_jwtuser import user_db, User, UserCreate, UserUpdate, UserDB

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
