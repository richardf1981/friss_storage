import sys
import uuid

from fastapi import FastAPI, Depends, Response
from fastapi_users import password
from loguru import logger
from starlette.staticfiles import StaticFiles

from .config import get_settings
from .datalayer.db import database, Base, engine, SessionLocal
from .datalayer.models_jwtuser import UserTable
from .dependencies import fastapi_users, jwt_authentication, logging_dependency
from .routers import router_file_api, router_ui

##############################################################################
# ADDING LOGGER
logger.remove()
logger.add(sys.stdout, colorize=True,
           format="<green>{time:HH:mm:ss}</green> | "
                  "{level} | <level>{message}</level>")
# END LOGGER
##############################################################################


##############################################################################
# STARTING APP MAIN
app = FastAPI(
    title="Friss - Document Management System - MVP",
    description="Project for upload/download of documents",
    version="0.0.1",
)
# END MAIN
##############################################################################


##############################################################################
# ADDING ROUTER FOR API
dependency_logging = []

if get_settings().logger_middleware_on:
    dependency_logging.append(Depends(logging_dependency))

app.include_router(router_file_api.router, dependencies=dependency_logging)
# END- ADDING ROUTER FOR API
##############################################################################


##############################################################################
# ADDING ROUTER FOR UI
#
app.include_router(router_ui.router)
app.mount("/static", StaticFiles(directory="app/templates/static"),
          name="static")
# END- ADDING ROUTER FOR UI
##############################################################################


@app.on_event("startup")
async def startup():
    await database.connect()
    Base.metadata.create_all(engine)
    # Add dummy user... TODO: should kept?
    session = None
    try:
        session = SessionLocal()
        user = UserTable(email='demouser@friss.com',
                         hashed_password=password.
                         get_password_hash('4w7ZFMAYF2nFmgUs'),
                         id=uuid.uuid4())
        session.add(user)
        session.commit()
        session.refresh(user)
    except Exception as ex:
        if session:
            session.rollback()
        logger.warning("Error creating user " + str(ex.__class__))

    # fix table charset...
    try:
        _session = SessionLocal()
        _session.execute("SET FOREIGN_KEY_CHECKS = 0")
        _session.execute("ALTER TABLE friss_storage.file_manager "
                         "CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        _session.execute("SET FOREIGN_KEY_CHECKS = 1")
        _session.close()
        logger.debug("charset changed successfully")
    except Exception as ex1:
        logger.warning("Error changing charset " + str(ex1.__class__))


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/refresh", tags=["auth"])
async def refresh_jwt(response: Response,
                      user=Depends(fastapi_users.get_current_active_user)):
    return await jwt_authentication.get_login_response(user, response)


app.include_router(
    fastapi_users.get_auth_router(jwt_authentication,
                                  requires_verification=False),
    prefix="",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(None), prefix="/auth", tags=["auth"]
)
