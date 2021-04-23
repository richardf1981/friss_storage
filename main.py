from fastapi import FastAPI, Depends, Response
from datalayer.db import database, Base, engine
from dependencies import fastapi_users, jwt_authentication
from routers import router_file_api

app = FastAPI(
    title="Friss - Document Management System - MVP",
    description="Project for upload/download of documents",
    version="0.0.1",
)

#dev_mode = bool(os.getenv("TEST", 0))
# dep = []

# if dev_mode is False:
#     dep.append(Depends(fastapi_users.get_current_active_user))

#app.include_router(file_api.router, dependencies=dep)
app.include_router(router_file_api.router)


@app.on_event("startup")
async def startup():
    await database.connect()
    Base.metadata.create_all(engine)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# TODO: path...
@app.post("/refresh", tags=["auth"])
async def refresh_jwt(response: Response,
                      user=Depends(fastapi_users.get_current_active_user)):
    return await jwt_authentication.get_login_response(user, response)


app.include_router(
    fastapi_users.get_auth_router(jwt_authentication,
                                  requires_verification=False),
    prefix="",  # TODO: path...
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(None), prefix="/auth", tags=["auth"]
)
