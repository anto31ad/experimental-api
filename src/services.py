import pickle
from logging import Logger

from .schema import Service, ServiceOutput


def _serve_iris(input_payload: dict, logger: Logger) -> ServiceOutput:

    with open('data/iris_classifier.pkl', 'rb') as file:
        logger.info("Attempting to load model")
        model = pickle.load(file)

    raw_prediction = model.predict([
        list(input_payload.values())
    ])

    prediction = int(raw_prediction[0])

    return ServiceOutput(
        input_payload=input_payload,
        output={
            'predicted-class-id': prediction
        }
    )


def _serve_digits(input_payload: dict, logger: Logger):

    with open('data/digit_classifier.pkl', 'rb') as file:
        logger.info("Attempting to load model")
        model = pickle.load(file)

    data_str = input_payload['pixels']
    data_points = [float(x) for x in data_str.split(";")]

    raw_prediction = model.predict([
        data_points
    ])

    prediction = int(raw_prediction[0])

    return ServiceOutput(
        input_payload=input_payload,
        output={
            'predicted-digit': prediction
        }
    )

SERVICES_CALLABLES = {
    'iris': _serve_iris,
    'digits': _serve_digits
}

def serve(service_id: str, args: dict, logger: Logger) -> ServiceOutput | None:

    callable = SERVICES_CALLABLES.get(service_id)
    if not callable:
        return None

    return callable(
        input_payload=args,
        logger=logger
    )
