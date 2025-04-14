import pickle

from http import HTTPStatus
from fastapi import FastAPI
from pydantic import BaseModel

class Flower(BaseModel):
    sepal_length: float = 0
    sepal_width: float = 0
    petal_length: float = 0
    petal_width: float = 0


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/predict")
def predict(features: Flower):

    with open('data/model.pkl', 'rb') as file:
        model = pickle.load(file)

    raw_prediction = model.predict(
        [
            [
                features.sepal_length,
                features.sepal_width,
                features.petal_length,
                features.petal_width,
            ]
        ]
    )
    prediction = int(raw_prediction[0])

    return {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": {
            "features": {
                "sepal_length": features.sepal_length,
                "sepal_width": features.sepal_width,
            },
            "prediction_id": prediction,
        },
    }
