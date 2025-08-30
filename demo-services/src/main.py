import os
import logging
import asyncio
import uuid
import consul
from typing import Dict
from contextlib import asynccontextmanager
from http import HTTPStatus
from fastapi import FastAPI, HTTPException

from .schema import Payload, IrisPayload, DigitsPayload
from .services import serve_digits, serve_iris

logger = logging.getLogger("uvicorn")

# Get configuration from environment variables
SERVICE_NAME = os.getenv("SERVICE_NAME", "no name")
SERVICE_HOST = os.getenv("SERVICE_HOST", "127.0.0.1")
SERVICE_PORT = int(os.getenv("SERVICE_PORT", "8000"))
CONSUL_HOST = os.getenv("CONSUL_HOST", "127.0.0.1")
CONSUL_PORT = int(os.getenv("CONSUL_PORT", "8500"))

# Generate a unique ID for the service instance
SERVICE_ID = f"{SERVICE_NAME}-{uuid.uuid4()}"

# Consul client instance
consul_client = consul.Consul(host=CONSUL_HOST, port=CONSUL_PORT)

# --- Service Registration/Deregistration Logic ---

async def register_service():
    """Register the service with Consul."""
    logger.info(f"Registering service '{SERVICE_NAME}' with ID '{SERVICE_ID}'...")

    # The health check tells Consul how to verify our service is healthy
    health_check = consul.Check.http(
        f"http://{SERVICE_HOST}:{SERVICE_PORT}/health",
        interval="10s",
        deregister="1m"
    )

    try:
        await asyncio.to_thread(
            consul_client.agent.service.register,
            name=SERVICE_NAME,
            address=SERVICE_HOST,
            service_id=SERVICE_ID,
            port=SERVICE_PORT,
            check=health_check
        )
        logger.info("Service registered successfully.")
    except Exception as e:
        logger.info(f"Failed to register service with Consul: {e}")
        # In a real-world scenario, you might want to retry or handle this error more gracefully


async def deregister_service():
    """Deregister the service from Consul."""
    logger.info(f"Deregistering service '{SERVICE_NAME}' with ID '{SERVICE_ID}'...")
    try:
        await asyncio.to_thread(consul_client.agent.service.deregister, service_id=SERVICE_ID)
        logger.info("Service deregistered successfully.")
    except Exception as e:
        logger.info(f"Failed to deregister service with Consul: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    """
    await register_service()
    try:
        yield
    finally:
        await deregister_service()

app = FastAPI(
    title='Experimental API / Demo models',
    lifespan=lifespan
)

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint for Consul."""
    return {"status": "ok"}

@app.get("/info")
async def get_service_info():
    return {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": {
            'name': 'Demo Services!',
            'description': "groups two models together: digits and iris",
            "parameters": [
                {
                    'name': 'model_id',
                    'description': "Takes 'digits' or 'iris'" 
                },
                {
                    'name': 'model_input',
                    'description': 'depending on model_id, the input data',
                    'examples': {
                        'Digits Example': {
                            'pixels': "0.0;0.0;10.0;16.0;16.0;11.0;0.0;0.0;0.0;1.0;11.0;"
                                      "7.0;6.0;16.0;3.0;0.0;0.0;0.0;0.0;0.0;10.0;15.0;0.0;0.0;"
                                      "0.0;0.0;0.0;0.0;15.0;7.0;0.0;0.0;0.0;0.0;0.0;0.0;15.0;"
                                      "9.0;0.0;0.0;0.0;0.0;0.0;0.0;7.0;13.0;0.0;0.0;0.0;0.0;"
                                      "5.0;4.0;10.0;16.0;0.0;0.0;0.0;0.0;10.0;16.0;16.0;10.0;0.0;0.0"
                        },
                        'Iris Example': {
                            'petal_length': 0,
                            'petal_width': 0,
                            'sepal_length': 0,
                            'sepal_width': 0
                        }
                    }
                }
            ]
        }
    }

@app.post("/use")
async def use_service(payload: Payload):

    result_data = {}

    try:
        if payload.model_id == 'digits':
            result_data = serve_digits(
                DigitsPayload(**payload.model_input),
                logger
            )
        elif payload.model_id == 'iris':
            result_data = serve_iris(
                IrisPayload(**payload.model_input),
                logger
            )
        else:
            raise Exception("Invalid Model ID")
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=str(e)
        )

    return {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": result_data
    }
