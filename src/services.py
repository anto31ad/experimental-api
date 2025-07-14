import http
import http.client
import requests
from logging import Logger
from urllib.parse import urlparse

from . import config
from . import utils
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
    
    url_hostname = parsed_url.hostname if parsed_url.hostname else ''
    if parsed_url.port:
        url_port = parsed_url.port
    elif parsed_url.scheme == "http":
        url_port = http.client.HTTP_PORT
    elif parsed_url.scheme == "https":
        url_port = http.client.HTTPS_PORT
    else:
        url_port = 0

    if utils.is_same_process(
        hostname_a  = url_hostname,
        port_a      = url_port,
        hostname_b  = config.THIS_HOST,
        port_b      = config.THIS_PORT
    ):
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
