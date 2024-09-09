from flask import Flask, request
from json  import dumps

app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'])
def log() -> dict:

    data = {
        'headers' : to_dict(request.headers),
        'args'    : to_dict(request.args),
        'form'    : to_dict(request.form),
        'files'   : to_dict(request.files),
        'json'    : request.json if request.is_json else {}
    }

    print(dumps(data, indent = 4))
    return data


def to_dict(data) -> dict:

    return data.to_dict(flat = False) if 'to_dict' in dir(data) else dict(data)
