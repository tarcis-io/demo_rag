from flask import Flask, request
from json  import dumps

app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def log():

    data = {
        'headers' : to_dict(request.headers),
        'args'    : to_dict(request.args),
        'form'    : to_dict(request.form),
        'files'   : to_dict(request.files),
        'json'    : request.json if request.is_json else {}
    }

    data = dumps(data, indent = 4)
    print(data)

    return data


def to_dict(data): return data.to_dict(flat = False) if 'to_dict' in dir(data) else dict(data)
