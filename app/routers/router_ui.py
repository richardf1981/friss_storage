from fastapi import APIRouter, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

from ..services.basicauth import BasicAuth, BasicAuthHelper

router = APIRouter(
    prefix="",
    responses={404: {"description": "Not found"}},
    tags=[""],
    include_in_schema=False
)

templates = Jinja2Templates(directory="app/templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

basic_auth = BasicAuth(auto_error=False)


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, auth: BasicAuth = Depends(basic_auth)):
    response = BasicAuthHelper.auth_basic(auth, request)

    if response == "DONE":
        return templates.TemplateResponse("index.html", {"request": request})
    else:
        return response
