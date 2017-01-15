import json
import jsonschema
from jsonschema.validators import validate
from model.measurementModel import MeasurementModel

schema = {
    "type": "object",
    "properties": {
        "ws_id": {"type": "integer"},
        "token": {"type": "string", "minLength": 5, "maxLength": 5},
        "time": {"type": "string"},
        "measurements": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "sensor_id": {"type": "integer"},
                    "value": {"type": "number"},
                },
                "required": ["sensor_id", "value"],
                "additionalProperties": False
            },
            "uniqueItems": True
        },
        "errors": {
            "type": "array",
            "items": {
            },
            "uniqueItems": True
        }
    },
    "required": ["ws_id", "token", "time", "measurements", "errors"],
    "additionalProperties": False
}

json_object = None


def is_correct_json(in_json):
    if is_json(in_json):
        try:
            validate(json_object, schema)
            return json_object
        except jsonschema.exceptions.ValidationError as ve:
            raise Exception(ve.message)
    raise Exception("Incorrect format of Json")


def is_json(in_json):
    global json_object
    try:
        json_object = json.loads(in_json)
    except ValueError, e:
        print e
        return False
    return True
