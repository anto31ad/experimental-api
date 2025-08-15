import logging
from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from .schema import IrisPayload, DigitsPayload
from .services import serve_digits, serve_iris

logger = logging.getLogger("uvicorn")

# setup FastAPI app
app = FastAPI(
    title='Experimental API / Demo models'
)

@app.post("/iris", tags=["Models"])
async def use_iris(
    payload: IrisPayload = IrisPayload(
        petal_length=0,
        petal_width=0,
        sepal_length=0,
        sepal_width=0
    )
):
    try:
        return {
            "message": HTTPStatus.OK.phrase,
            "status-code": HTTPStatus.OK,
            "data": serve_iris(payload, logger)
        }

    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    

@app.post("/digits", tags=["Models"])
async def use_digits(
    payload: DigitsPayload = DigitsPayload(
        pixels="0.0;0.0;10.0;16.0;16.0;11.0;0.0;0.0;0.0;1.0;11.0;"
                "7.0;6.0;16.0;3.0;0.0;0.0;0.0;0.0;0.0;10.0;15.0;0.0;0.0;"
                "0.0;0.0;0.0;0.0;15.0;7.0;0.0;0.0;0.0;0.0;0.0;0.0;15.0;"
                "9.0;0.0;0.0;0.0;0.0;0.0;0.0;7.0;13.0;0.0;0.0;0.0;0.0;"
                "5.0;4.0;10.0;16.0;0.0;0.0;0.0;0.0;10.0;16.0;16.0;10.0;0.0;0.0"
    )
):
    try:
        return {
            "message": HTTPStatus.OK.phrase,
            "status-code": HTTPStatus.OK,
            "data": serve_digits(payload, logger)
        }
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
