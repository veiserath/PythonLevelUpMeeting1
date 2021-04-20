from fastapi import FastAPI, Response, status
from pydantic import BaseModel
import datetime
from datetime import date

app = FastAPI()
app.counter = 1
app.patients = list()


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
    print(days)
    timedifference = datetime.timedelta(days=days)
    end_date = start_date + timedifference
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    data_set = {"id": app.counter, "name": modified_details.name, "surname": modified_details.surname,
                "register_date": start_date, "vaccination_date": end_date}
    app.patients.append(data_set)
    app.counter += 1
    return data_set


@app.get("/patient/{id}")
def patient(response: Response, id):
    response.status_code = status.HTTP_200_OK
    for dictionary in app.patients:
        if dictionary["id"] == id:
            return dictionary
        if dictionary["id"] < 1:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return
    response.status_code = status.HTTP_404_NOT_FOUND
    return


# some_list = list()
#
# data_set = {"id": 1, "name": "Michal", "surname": "Markowicz",
#                 "register_date": "2021-04-20", "vaccination_date": "2021-05-06"}
#
# some_list.append(data_set)
# for dictionary in some_list:
#         if dictionary["id"] == 1:
#             print(dictionary)
