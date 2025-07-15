from pydantic import BaseModel

class IrisPayload(BaseModel):
    petal_length: float
    petal_width: float
    sepal_length: float
    sepal_width: float

class DigitsPayload(BaseModel):
    pixels: str
