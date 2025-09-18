from pydantic import BaseModel

class Payload(BaseModel):
    model_id: str
    model_input: dict

class DigitsPayload(BaseModel):
    pixels: str
