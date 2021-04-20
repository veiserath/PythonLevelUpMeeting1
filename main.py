import hashlib

from fastapi import FastAPI,Response,status

app = FastAPI()


@app.get("/auth")
def get(password: str, password_hash: str, response: Response):
    response.status_code = status.HTTP_401_UNAUTHORIZED
    if password is None or password_hash is None:
        return
    encrypted = hashlib.sha512(str(password).encode("utf-8")).hexdigest()
    if encrypted == password_hash:
        response.status_code = status.HTTP_204_NO_CONTENT
        return
    return
