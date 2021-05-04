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

templates = Jinja2Templates(directory='templates')


@app.get("/hello", response_class=HTMLResponse)
def root(request: Request):
    today = date.today().strftime("%Y-%m-%d")
    return templates.TemplateResponse('index.html', {'request': request, 'today': today})


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.post("/login_session")
def read_current_user(response: Response, username=Depends(get_current_username)):
    # app.tokens_login_session.clear()
    # app.tokens_login_session.append('abc')
    token_value1.append('z')
    str1 = ''
    for i in token_value1:
        str1 += 'z'
    if len(app.tokens_login_session) < 3:
        app.tokens_login_session.append(str1)
    else:
        app.tokens_login_session[0] = app.tokens_login_session[1]
        app.tokens_login_session[1] = app.tokens_login_session[2]
        app.tokens_login_session[2] = str1
    print(f'{str1}')
    response.set_cookie(key='session_token', value=str1)
    response.status_code = status.HTTP_201_CREATED
    print(f'{app.tokens_login_session}')
    return {'username': username}


@app.post("/login_token")
def read_current_user(response: Response, username=Depends(get_current_username)):
    token_value.append('a')
    str1 = ''
    for i in token_value:
        str1 += 'a'
    if len(app.tokens_login_token) < 3:
        app.tokens_login_token.append(str1)
    else:
        app.tokens_login_token[0] = app.tokens_login_token[1]
        app.tokens_login_token[1] = app.tokens_login_token[2]
        app.tokens_login_token[2] = str1

    response.set_cookie(key="session_token", value=str1)
    response.status_code = status.HTTP_201_CREATED
    print(f'{app.tokens_login_token}')
    return {'token': str1}


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
    if [i for i in token if i in app.tokens_login_token] == []:
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
def logout_session(response: Response, session_token: str = Cookie(None), format: Optional[str] = None):
    if session_token not in app.tokens_login_session:
        response.status_code = 401
        return response
    app.tokens_login_session.remove(session_token)
    url = f'/logged_out?format={format}'
    response.status_code = 302
    return RedirectResponse(url=url, status_code=302)


@app.delete("/logout_token")
def logout_token(response: Response, token: List[str] = Query(None), format: Optional[str] = None):
    if not [i for i in token if i in app.tokens_login_token]:
        raise HTTPException(status_code=401, detail="Unauthorised")
    app.tokens_login_token.remove(token)
    url = f'/logged_out?format={format}'
    response.status_code = 302
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

