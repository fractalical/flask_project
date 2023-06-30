from flask import Flask, jsonify

from service import HttpError
from views import UserView, UserAuthView

app = Flask('app')


@app.errorhandler(HttpError)
def http_error_handler(error: HttpError):
    error_message = {
        'status': 'error',
        'description': error.message
    }
    response = jsonify(error_message)
    response.status_code = error.status_code
    return response


app.add_url_rule('/user/<int:user_id>',
                 view_func=UserView.as_view('with_user_id'),
                 methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/user/',
                 view_func=UserView.as_view('create_user'),
                 methods=['POST'])
app.add_url_rule('/auth_user/',
                 view_func=UserAuthView.as_view('auth_user'),
                 methods=['POST'])
