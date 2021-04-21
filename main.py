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


@app.post("/register")
def register(response: Response, modified_details: ModifiedDetails):
    response.status_code = status.HTTP_201_CREATED
    start_date = date.today()
    counter = 0
    i = 0
    for character in modified_details.name:
        if i == 0 and 'A' <= character <= 'Z':
            counter += 1
        elif 'a' <= character <= 'z':
            counter += 1
    i = 0
    for character in modified_details.surname:
        if i == 0 and 'A' <= character <= 'Z':
            counter += 1
        elif 'a' <= character <= 'z':
            counter += 1
    timedifference = datetime.timedelta(days=counter)
    end_date = start_date + timedifference
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    data_set = {"id": app.counter, "name": modified_details.name, "surname": modified_details.surname,
                "register_date": start_date, "vaccination_date": end_date}
    app.counter += 1
    return data_set