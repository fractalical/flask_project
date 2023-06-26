from hashlib import md5

from flask import jsonify, request, Flask
from pydantic import ValidationError

from schema import VALIDATION_CLASS
from views import UserView

app = Flask('app')


class HttpError(Exception):

    def __init__(self, status_code: int, message: dict | list | str):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def http_error_handler(error: HttpError):
    error_message = {
        'status': 'error',
        'description': error.message
    }
    response = jsonify(error_message)
    response.status_code = error.status_code
    return response


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


app.add_url_rule('/user/<int:user_id>',
                 view_func=UserView.as_view('with_user_id'),
                 methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/user/',
                 view_func=UserView.as_view('create_user'),
                 methods=['POST'])
