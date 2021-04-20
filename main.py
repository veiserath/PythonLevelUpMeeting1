from fastapi import FastAPI

app = FastAPI()

@app.get("/method")
def get():
    return {"method": "GET"}
@app.put("/method")
def put():
    return {"method": "PUT"}
@app.options("/method")
def options():
    return {"method": "OPTIONS"}
@app.delete("/method")
def delete():
    return {"method": "DELETE"}
@app.post("/method", status_code=201)
def post():
    return {"method": "POST"}
