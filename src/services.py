import pickle
from logging import Logger

from schema import Service, ServiceOutput

def serve(service: Service, args: dict, logger: Logger) -> ServiceOutput:
    
    errors_list: list[str] = []

    feature_names = [p.name for p in service.parameters]
    feat_dic = {key: args[key] for key in feature_names if key in args}

    with open(service.path_to_model, 'rb') as file:
        logger.info("Attempting to load model")
        model = pickle.load(file)

    try:
        raw_prediction = model.predict([
            list(feat_dic.values())
        ])
    except Exception as e:
        errors_list.append(str(e))

    if errors_list:
        return ServiceOutput(
            input_payload=feat_dic,
            errors=errors_list
        )

    prediction = int(raw_prediction[0])

    return ServiceOutput(
        input_payload=feat_dic,
        output={
            'predicted-class-id': prediction
        }
    )
