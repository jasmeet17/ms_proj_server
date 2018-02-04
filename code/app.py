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
import differentiate
import aws_bucket



app = Flask(__name__)
dtw = differentiate.DTW()
aws = aws_bucket.AwsBucket()

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

TEMP_FOLDER = 'static/tmp'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','mp3'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = TEMP_FOLDER

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
        up_file = request.files['audio_file']
        filename = secure_filename(up_file.filename)
        upload_filename = 'x'+ filename
        if not saveUploadedFile(up_file, upload_filename):
            response = REQUEST_FAIL
            # response['error'] = 'Upload fail.'
            response['error'] = upload_filename
        elif not aws.downloadFile(filename):
            response = REQUEST_FAIL
            response['error'] = 'Unable to get file from Server.'
        elif not dtw.differntiateFile(filename, upload_filename):
            response = REQUEST_FAIL
            response['error'] = 'Unable to compare at the moment.'
        else:
            response = REQUEST_SUCCESS
            fig_image = upload_filename.replace('.flac')
            response['image_url'] = request.host_url + UPLOAD_FOLDER +'/' + fig_image +'.png'

    return jsonify(response)

def saveUploadedFile(upfile, filename):
    saved_status = False
    if filename.strip=='':
        return saved_status

    try:
        upFile.save(os.path.join(app.config['UPLOAD_FOLDER'], 'x'+filename))
        saved_status = True
    except Exception as e:
        print('Cannot save Upladed file')
        saved_status = False
    return saved_status


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0')