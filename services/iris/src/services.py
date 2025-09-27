import pickle
from logging import Logger
from sklearn.datasets import load_iris

from .schema import IrisPayload


def serve_iris(input_payload: IrisPayload, logger: Logger) -> int:

    iris_data = load_iris()
    iris_species_map = {i: name for i, name in enumerate(iris_data.target_names)}

    with open('data/models/iris_classifier.pkl', 'rb') as file:
        logger.info("Attempting to load model")
        model = pickle.load(file)

    raw_prediction = model.predict([
        list(input_payload.model_dump().values())
    ])

    prediction = int(raw_prediction[0])
    prediction_name = iris_species_map.get(prediction, "unknown")
    return prediction_name
