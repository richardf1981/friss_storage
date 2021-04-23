##
# This is a pretty ugly object for basic auth...
# I believe it was easier and something ready to use
##

import base64
from datetime import timedelta, datetime
from typing import Optional

import jwt
from fastapi import Request, HTTPException, Response
from fastapi.encoders import jsonable_encoder
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param
from starlette.responses import RedirectResponse
from starlette.status import HTTP_403_FORBIDDEN

from ..dependencies import SECRET_JWT

USER_NAME_BASIC = "demouser@friss.com"
PASSWORD_BASIC = "4w7ZFMAYF2nFmgUs"


class BasicAuth(SecurityBase):
    def __init__(self, scheme_name: str = None, auto_error: bool = True):
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)

        if not authorization or scheme.lower() != "basic":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None
        return param


class BasicAuthHelper:

    @staticmethod
    def create_access_token(*, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_JWT, algorithm='HS256')
        return encoded_jwt

    @staticmethod
    def auth_basic(auth, request):
        if not auth:
            response = Response(headers={"WWW-Authenticate": "Basic"},
                                status_code=401)
            return response

        try:
            decoded = base64.b64decode(auth).decode("ascii")
            username, _, password = decoded.partition(":")

            if username != USER_NAME_BASIC or password != PASSWORD_BASIC:
                raise HTTPException(status_code=400,
                                    detail="Incorrect email or password")

            access_token_expires = timedelta(minutes=40)
            access_token = BasicAuthHelper.create_access_token(
                data={"sub": username}, expires_delta=access_token_expires
            )

            token = jsonable_encoder(access_token)

            response = RedirectResponse(url="/")
            response.set_cookie(
                "Authorization",
                value=f"Bearer {token}",
                domain="local",
                httponly=True,
                max_age=180000,
                expires=180000,
            )
            return "DONE"
        except Exception:
            response = Response(headers={"WWW-Authenticate": "Basic"},
                                status_code=401)
            return response
