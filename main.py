from hashlib import sha256
from fastapi import FastAPI, Response, Cookie, HTTPException, status

app = FastAPI()
app.secret_key = "very constatn and random secret, best 64+ characters"
app.access_tokens = []


@app.post("/login_session")
def login(user: str, password: str, response: Response):
    login_name = "4dm1n"
    password_name = "NotSoSecurePa$$"
    if user == login_name and password == password_name:
        session_token = sha256(f"{user}{password}{app.secret_key}".encode()).hexdigest()
        app.access_tokens.append(session_token)
        response.set_cookie(key="session_token", value=session_token)
        response.status_code = status.HTTP_201_CREATED
        return response
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED


@app.post("/login_token")
def secured_data(*, response: Response, session_token: str = Cookie(None)):
    if session_token not in app.access_tokens:
        raise HTTPException(status_code=401, detail="Unathorised")
    else:
        app.access_tokens.remove(session_token)
        return {"token": session_token}