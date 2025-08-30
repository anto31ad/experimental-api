from pydantic import BaseModel

class Payload(BaseModel):
    model_id: str
    model_input: dict

class IrisPayload(BaseModel):
    petal_length: float
    petal_width: float
    sepal_length: float
    sepal_width: float

class DigitsPayload(BaseModel):
    pixels: str
