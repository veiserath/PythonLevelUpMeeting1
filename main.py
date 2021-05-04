from hashlib import sha256
from fastapi import FastAPI, Response, Cookie, HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
app.secret_key = "very constatn and random secret, best 64+ characters"
app.access_tokens = []

security = HTTPBasic()


@app.post("/login_session")
def login(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    user = credentials.username
    password = credentials.password
    if user == "4dm1n" and password == "NotSoSecurePa$$":
        session_token = sha256(f"{user}{password}{app.secret_key}".encode()).hexdigest()
        app.access_tokens.append(session_token)
        response.set_cookie(key="session_token", value=session_token)
        response.status_code = status.HTTP_201_CREATED
        return response
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response


@app.post("/login_token")
def secured_data(response: Response, session_token: str = Cookie(None),
                 credentials: HTTPBasicCredentials = Depends(security)):
    user = credentials.username
    password = credentials.password
    if user == '4dm1n' and password == 'NotSoSecurePa$$':
        session_token = app.secret_key_sample + str(app.composition_to_key)
        app.session_token = session_token
        app.composition_to_key += 1
        response.set_cookie(key='session_token', value=session_token)
        return {"token": app.session_token}
    if session_token in app.access_tokens:
        app.access_tokens.remove(session_token)
        response.status_code = status.HTTP_201_CREATED
        return {"token": session_token}
    if session_token not in app.access_tokens:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response
