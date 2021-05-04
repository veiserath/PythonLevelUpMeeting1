from fastapi import FastAPI, Request, Depends, HTTPException, status, Cookie, Response, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import List, Optional
import secrets
from datetime import date
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse, RedirectResponse

app = FastAPI()
# app.secret_key = "very constatn and random secret, best 64+ characters"
app.tokens_login_token = []
app.tokens_login_session = []
token_value = []
token_value1 = []
security = HTTPBasic()


@app.get("/welcome_session", status_code=200)
def func(*, response: Response, session_token: str = Cookie(None), format: Optional[str] = None):
    print(f'{app.tokens_login_session}')
    if session_token not in app.tokens_login_session:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response
    if format == 'json':
        return JSONResponse({"message": "Welcome!"})
    if format == 'html':
        return HTMLResponse("""
    <html>
        <head>
        </head>
        <body>
            <h1>Welcome!</h1>
        </body>
    </html>
    """)
    else:
        return PlainTextResponse("Welcome!")


@app.get("/welcome_token", status_code=200)
def func(response: Response, token: List[str] = Query(None), format: Optional[str] = None):
    if not [i for i in token if i in app.tokens_login_token]:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response
    if format == 'json':
        return JSONResponse({"message": "Welcome!"})
    if format == 'html':
        return HTMLResponse("""
    <html>
        <head>
        </head>
        <body>
            <h1>Welcome!</h1>
        </body>
    </html>
    """)
    else:
        return PlainTextResponse("Welcome!")
