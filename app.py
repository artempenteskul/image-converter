import os

from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

from utils import generate_id_for_file, get_filename_from_file_id


UPLOAD_FOLDER = 'media'
UPLOAD_FOLDER_ORIGINAL = 'media/100'

app = Flask(__name__)


if not os.path.exists('media'):
    os.makedirs('media')


@app.route('/', methods=['GET'])
def healthcheck():
    resp = jsonify({'message': 'Up and running'})
    resp.status_code = 200
    return resp


@app.route('/upload/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 404
        return resp

    file_id = generate_id_for_file()

    os.makedirs(os.path.join(UPLOAD_FOLDER_ORIGINAL, file_id))

    file = request.files['file']
    file.save(os.path.join(UPLOAD_FOLDER_ORIGINAL, file_id, secure_filename(file.filename)))

    return jsonify({'message': 'success', 'file_id': file_id})


@app.route('/download/<path:file_id>/', methods=['GET'])
def download_file(file_id):
    quality = request.args.get('quality', '100')
    if quality not in ('100', '75', '50', '25'):
        resp = jsonify({'message': 'Incorrect quality value. Supported values: 100, 75, 50 and 25.'})
        resp.status_code = 400
        return resp

    filename = get_filename_from_file_id(file_id)
    return send_from_directory(os.path.join(UPLOAD_FOLDER, quality, file_id), filename)
