import os
import json
import random
import string

from logging import Logger

from .schema import Service

RANDOM_STRING_CHARS = string.ascii_letters + string.digits

def save_services(logger: Logger, services: dict[str, Service]):
    try:
        # create directory if doesn't exist already
        os.makedirs("data", exist_ok=True)
    except Exception as e:
        logger.error("error while creating directory", e)

    try:
        # save the services dictionary to file
        with open('data/services.json', "w") as file:
            json.dump({k: v.model_dump() for k, v in services.items()}, file)
    except Exception as e:
        logger.error("error while writing database", e)


def load_services(logger: Logger) -> dict[str, Service]:

    # if there is no services file, return empty dict 
    if not os.path.exists('data/services.json'):
        return {}
    # otherwise, try to read its contents
    try:
        with open('data/services.json', "r") as file:
            data = json.load(file)
            return {k: Service.model_validate(v) for k, v in data.items()}
    except Exception as e:
        logger.error(e)
        return {}


def create_service(
    logger: Logger,
    services: dict[str, Service],
    new_service: Service,
) -> str | None:
    # try to generate a random string for the id
    id = None
    for attempt in range(1, 100):
        id = ''.join(random.choices(RANDOM_STRING_CHARS, k=6))
        # check conflicts
        if id in services:
            id = None
            continue
        else:
            break
    # if every attempt generated a conflicting string, raise exception
    if not id:
        logger.error("Exceded maximum number of attemps while generating unique ID for a service")
        return None
    # update the dictionary in place
    services[id] = new_service
    return id
