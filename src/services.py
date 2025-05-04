import pickle
from logging import Logger

from .schema import Service, ServiceOutput


def _serve_iris(input_payload: dict, logger: Logger) -> ServiceOutput:

    with open('data/iris_classifier.pkl', 'rb') as file:
        logger.info("Attempting to load model")
        model = pickle.load(file)

    try:
        raw_prediction = model.predict([
            list(input_payload.values())
        ])
    except Exception as e:
        return ServiceOutput(
            input_payload=input_payload,
            errors=[str(e)]
        )

    prediction = int(raw_prediction[0])

    return ServiceOutput(
        input_payload=input_payload,
        output={
            'predicted-class-id': prediction
        }
    )


def _serve_digits(input_payload: str, logger: Logger):

    with open('data/digit_classifier.pkl', 'rb') as file:
        logger.info("Attempting to load model")
        model = pickle.load(file)

    data_str = input_payload['pixels']
    data_points = [float(x) for x in data_str.split(";")]

    try:
        raw_prediction = model.predict([
            data_points
        ])
    except Exception as e:
        return ServiceOutput(
            input_payload=input_payload,
            errors=[str(e)]
        )

    prediction = int(raw_prediction[0])

    return ServiceOutput(
        input_payload=input_payload,
        output={
            'predicted-digit': prediction
        }
    )

SERVICES_CALLABLES = {
    1: _serve_iris,
    2: _serve_digits
}

def serve(service: Service, args: dict, logger: Logger) -> ServiceOutput:

    feature_names = [p.name for p in service.parameters]
    feat_dic = {key: args[key] for key in feature_names if key in args}

    return SERVICES_CALLABLES[service.id](
        input_payload=feat_dic,
        logger=logger
    )
