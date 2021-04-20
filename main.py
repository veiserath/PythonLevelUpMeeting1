import hashlib

from fastapi import FastAPI, Response, status

app = FastAPI()


@app.get("/auth")
def get(response: Response, password: str = None, password_hash: str = None):

    # if password is None or password_hash is None:
    #     return
    encrypted = hashlib.sha512(str(password).encode("utf-8")).hexdigest()
    if encrypted == password_hash:
        response.status_code = status.HTTP_204_NO_CONTENT
        return
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return
