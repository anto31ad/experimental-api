import pickle
from logging import Logger

from .schema import DigitsPayload

def serve_digits(input_payload: DigitsPayload, logger: Logger) -> int:

    with open('data/models/digit_classifier.pkl', 'rb') as file:
        logger.info("Attempting to load model")
        model = pickle.load(file)

    data_str = input_payload.pixels
    data_points = [float(x) for x in data_str.split(";")]

    raw_prediction = model.predict([
        data_points
    ])

    prediction = int(raw_prediction[0])

    return prediction
