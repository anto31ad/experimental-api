import pickle
import requests
from logging import Logger
from urllib.parse import urlparse

from . import config
from .schema import Service, ServiceOutput

def serve(service: Service, input_payload: dict, logger: Logger) -> ServiceOutput:

    executable_url = service.executable_url

    if not executable_url:
        return ServiceOutput(
            errors=[
                "Executable URL is missing."
            ]
        )

    parsed_url = urlparse(executable_url)
    if not parsed_url.scheme or not parsed_url.netloc:
        logger.error("Invalid Executable URL!")
        return ServiceOutput(
            errors=[
                "Executable URL is invalid."
            ]
        )
    
    # TODO samehost does not accound for aliases (e.g. localhost, 127.0.0.1, ...)
    same_host = parsed_url.hostname == config.THIS_HOST 
    same_port = parsed_url.port == int(config.THIS_PORT)
    logger.info(f"{same_host} {same_port}")
    if same_host and same_port:
        logger.error("Requesting path operation on this server")
        return ServiceOutput(
            errors=[
                "Cannot perform a path operation on this server while this request is running because it causes deadlock."
            ]
        )

    try:
        response = requests.post(url=executable_url, json=input_payload)
        # raise an exception if response has an error status
        response.raise_for_status()
        result = response.json()
        return ServiceOutput(
            input_payload=input_payload,
            output=result
        )
    except Exception as e:
        logger.error(f"Request failed: {e}")
        return ServiceOutput(
            errors=[
                str(e)
            ]
        )
