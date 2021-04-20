from urllib.request import Request
from fastapi import FastAPI, Response, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette.responses import JSONResponse
import datetime
from datetime import timedelta
from datetime import date
import json

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
    days = len(modified_details.name) + len(modified_details.surname)
    timedifference = datetime.timedelta(days=days)
    end_date = start_date + timedifference
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    data_set = {"id": app.counter, "name": modified_details.name, "surname": modified_details.surname,
                "register_date": start_date, "vaccination_date": end_date}
    # json_dump = json.dumps(data_set)
    # item = Details(app.counter, modified_details.name, modified_details.surname, start_date, end_date)
    # json_compatible_item_data = jsonable_encoder(item)
    app.counter += 1
    return data_set
