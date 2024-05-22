from fastapi import FastAPI, HTTPException
from interface import * 

app = FastAPI()

@app.get("/")
async def index():
    return {'message':'Hello world'}

@app.get("/properties/{zipcode}")
async def getProperties(zipcode:str):
    properties = pageRequest(zipcode)
    if not properties:
        raise HTTPException(status_code=404,detail='Information unavailable')
    return {"properties": properties}