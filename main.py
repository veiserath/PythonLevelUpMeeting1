import hashlib

from fastapi import FastAPI,Response,status

app = FastAPI()


@app.get("/auth", status_code=204)
def get(password: str, password_hash: str, response: Response):
    encrypted = hashlib.sha512(str(password).encode("utf-8")).hexdigest()
    if encrypted == password_hash:
        response.status_code = status.HTTP_204_NO_CONTENT
        return
    response.status_code = status.HTTP_401_UNAUTHORIZED
    return
