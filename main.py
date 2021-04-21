import hashlib
from fastapi import FastAPI, Response, status
from pydantic import BaseModel
import datetime
from datetime import date

app = FastAPI()
app.counter = 1


class Details(BaseModel):
    id: int
    name: str
    surname: str
    register_date: str
    vaccination_date: str


def __init__(self, id, name, surname, register_date, vaccination_date):
    self.id = id
    self.name = name
    self.surname = surname
    self.register_date = register_date
    self.vaccination_date = vaccination_date


class ModifiedDetails(BaseModel):
    name: str
    surname: str


@app.get("/auth")
def get(response: Response, password: str = None, password_hash: str = None):
    response.status_code = status.HTTP_401_UNAUTHORIZED
    if password is None or password_hash is None or password is "" or password_hash is "":
        return
    encrypted = hashlib.sha512(str(password).encode("utf-8")).hexdigest()
    if encrypted == password_hash:
        response.status_code = status.HTTP_204_NO_CONTENT
        return
    response.status_code = status.HTTP_401_UNAUTHORIZED
    return


@app.post("/register")
def register(response: Response, modified_details: ModifiedDetails):
    response.status_code = status.HTTP_201_CREATED
    start_date = date.today()
    counter = 0
    for character in modified_details.name:
        if 'A' <= character <= 'Z' or 'a' <= character <= 'z':
            counter += 1
    for character in modified_details.surname:
        if 'A' <= character <= 'Z' or 'a' <= character <= 'z':
            counter += 1
    timedifference = datetime.timedelta(days=counter)
    end_date = start_date + timedifference
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    data_set = {"id": app.counter, "name": modified_details.name, "surname": modified_details.surname,
                "register_date": start_date, "vaccination_date": end_date}
    app.counter += 1
    return data_set
