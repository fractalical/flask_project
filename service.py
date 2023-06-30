from hashlib import md5

from flask import jsonify
from pydantic import ValidationError

from schema import VALIDATION_CLASS


class HttpError(Exception):

    def __init__(self, status_code: int, message: dict | list | str):
        self.status_code = status_code
        self.message = message


def validate_json(json_data: dict, validation_model: VALIDATION_CLASS):
    try:
        model_obj = validation_model(**json_data)
        model_obj_dict = model_obj.dict()
    except ValidationError as err:
        raise HttpError(400, message=err.errors())
    return model_obj_dict


def hash_password(password: str):
    password = password.encode()
    password_hash = md5(password)
    return password_hash.hexdigest()