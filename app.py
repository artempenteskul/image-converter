import os
import json

from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

from utils import QualityEnum, generate_id_for_file, get_filename_from_file_id, send_message_to_rabbitmq


# TODO: overall refactoring
# TODO: make better structure for the project (add running with gunicorn and containerize with docker)


# TODO: move these hardcoded variables to the env variables / config files
UPLOAD_FOLDER = 'media'


app = Flask(__name__)


for q in QualityEnum:
    if not os.path.exists(f'media/{q.value}'):
        os.makedirs(f'media/{q.value}')


@app.route('/healthcheck/', methods=['GET'])
def healthcheck():
    resp = jsonify({'message': 'Up and running'})
    resp.status_code = 200
    return resp


@app.route('/upload/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp

    file = request.files['file']
    file_id = generate_id_for_file()
    filename = file.filename

    # TODO: make try/except block for this logic

    os.makedirs(os.path.join(UPLOAD_FOLDER, QualityEnum.HUNDRED.value, file_id))

    file.save(os.path.join(UPLOAD_FOLDER, QualityEnum.HUNDRED.value, file_id, secure_filename(filename)))

    send_message_to_rabbitmq(json.dumps({'file_id': file_id, 'filename': filename}))

    return jsonify({'message': 'success', 'file_id': file_id})


@app.route('/download/<path:file_id>/', methods=['GET'])
def download_file(file_id):
    quality = request.args.get('quality', QualityEnum.HUNDRED.value)
    if quality not in (q.value for q in QualityEnum):
        resp = jsonify({'message': 'Incorrect quality value. Supported values: 100, 75, 50 and 25.'})
        resp.status_code = 400
        return resp

    # TODO: check whether file with this file_id exists

    filename = get_filename_from_file_id(file_id)
    return send_from_directory(os.path.join(UPLOAD_FOLDER, quality, file_id), filename)
