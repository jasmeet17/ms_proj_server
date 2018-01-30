#!flask/bin/python
from flask import Flask
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
import logging
from logging.handlers import RotatingFileHandler
from werkzeug import secure_filename

import os
from flask import redirect, url_for



app = Flask(__name__)

UPLOAD_FOLDER = 'static/tmp'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','mp3'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

REQUEST_SUCCESS = {'result': 1}
REQUEST_FAIL = {'result': 0, 'error':''}


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found - 404'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad Request - 400'}), 400)

@app.route('/')
def index():
    return "Proje"

@app.route('/upload',methods=['PUT'])
def upload():
    # file = request.files['file_image']
    # newFile = FileContents(name=file.filename, date=file.read())
    response = {}
    if not request.files:
        response = REQUEST_FAIL
        response['error'] = "Audio file not found."
    else:
        upFile = request.files['audio_file']
        filename = secure_filename(upFile.filename)
        upFile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        response = REQUEST_SUCCESS
        response['image_url'] = request.host_url + "static/tmp/sample.jpg"

    return jsonify(response)


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0')