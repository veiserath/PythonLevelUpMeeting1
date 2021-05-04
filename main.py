from fastapi import FastAPI, Request, Depends, HTTPException, status, Cookie, Response,Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import List, Optional
import secrets
from datetime import date
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse, RedirectResponse

app = FastAPI()
app.secret_key_sample = 'qwerty'
app.composition_to_key = 1
app.session_token = ''

security = HTTPBasic()

app.tokens_login_token = []
app.tokens_login_session = []
token_value = []
token_value1 = []
security = HTTPBasic()


@app.get("/hello", response_class=HTMLResponse)
def index_static():
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Hello! Today date is 2021-05-04</h1>
        </body>
    </html>
    """


@app.post("/login_session", status_code=201)
def create_login_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    login = credentials.username
    password = credentials.password
    if login == '4dm1n' and password == 'NotSoSecurePa$$':
        session_token = app.secret_key_sample + str(app.composition_to_key)
        app.session_token = session_token
        app.composition_to_key += 1
        response.set_cookie(key='session_token', value=session_token)
    else:
        response.status_code = 401
        return response


@app.post("/login_token", status_code=201)
def get_login_token(response: Response, session_token: str = Cookie(None)
                    , credentials: HTTPBasicCredentials = Depends(security)):
    login = credentials.username
    password = credentials.password
    if login == '4dm1n' and password == 'NotSoSecurePa$$':
        session_token = app.secret_key_sample + str(app.composition_to_key)
        app.session_token = session_token
        app.composition_to_key += 1
        response.set_cookie(key='session_token', value=session_token)
        return {"token": app.session_token}

    if session_token == app.session_token:
        return {"token": app.session_token}

    response.status_code = 401
    return response


@app.get("/welcome_session")
def func(*, response: Response, session_token: str = Cookie(None), format: Optional[str] = None):
    print(f'{app.tokens_login_session}')
    if session_token not in app.tokens_login_session:
        raise HTTPException(status_code=401, detail="Unathorised")
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


@app.get("/welcome_token")
def func(token: List[str] = Query(None), format: Optional[str] = None):
    if not [i for i in token if i in app.tokens_login_token]:
        raise HTTPException(status_code=401, detail="Unathorised")
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


@app.delete("/logout_session")
def logout_session(request: Request, session_token: str = Cookie(None),format: Optional[str] = None):
    if session_token not in app.tokens_login_session:
        raise HTTPException(status_code=401, detail="Unathorised")
    app.tokens_login_session.remove(session_token)
    url = f'/logged_out?format={format}'
    return RedirectResponse(url=url, status_code=302)


@app.delete("/logout_token")
def logout_token(request: Request, token: List[str] = Query(None),format: Optional[str] = None):
    if not [i for i in token if i in app.tokens_login_token]:
        raise HTTPException(status_code=401, detail="Unauthorised")
    app.tokens_login_token.remove(token)
    url = f'/logged_out?format={format}'
    return RedirectResponse(url=url, status_code=302)


@app.get("/logged_out")
def logged_out(format: Optional[str] = None):
    if format == 'json':
        return JSONResponse({"message": "Logged out!"})
    if format == 'html':
        return HTMLResponse("""
    <html>
        <head>
        </head>
        <body>
            <h1>Logged out!</h1>
        </body>
    </html>
    """)
    else:
        return PlainTextResponse("Logged out!")
