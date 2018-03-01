#!flask/bin/python
from flask import Flask
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
import logging
from logging.handlers import RotatingFileHandler
from werkzeug import secure_filename
from logging import FileHandler, WARNING

import os
from flask import redirect, url_for
import differentiate
import aws_bucket
# import logs



app = Flask(__name__)
dtw = differentiate.DTW()



TEMP_FOLDER = 'static/tmp'
LOG_FOLDER = 'static/logs/'
AUDIO_EXCEL_FILE = 'audio_files_list.xlsx'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','mp3','xlsx'])

app = Flask(__name__)
app.debug = True
app.config['UPLOAD_FOLDER'] = TEMP_FOLDER
file_handler = FileHandler(LOG_FOLDER +'error-log.log')
file_handler.setLevel(WARNING)
app.logger.addHandler(file_handler)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.FileHandler(LOG_FOLDER + 'debugging_logs.log')

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
    response = REQUEST_SUCCESS
    if not fileExists(TEMP_FOLDER, AUDIO_EXCEL_FILE):
        aws = aws_bucket.AwsBucket()        
        if not aws.downloadFile(AUDIO_EXCEL_FILE):
            response = REQUEST_FAIL
            response['error'] = 'Unable to download file from Server.'
    return jsonify(response)

@app.route('/upload',methods=['PUT'])
def upload():
    # file = request.files['file_image']
    # newFile = FileContents(name=file.filename, date=file.read())
    aws = aws_bucket.AwsBucket()
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
            response['error'] = 'Upload fail.'
        elif not aws.downloadFile(filename):
            response = REQUEST_FAIL
            response['error'] = 'Unable to download file from Server.'
        elif not dtw.differntiateFile(filename, upload_filename):
            response = REQUEST_FAIL
            response['error'] = 'Unable to compare at the moment.'
        else:
            response = REQUEST_SUCCESS
            fig_image = upload_filename.replace('.flac','')
            response['image_url'] = request.host_url + TEMP_FOLDER +'/' + fig_image +'.png'

    return jsonify(response)

def saveUploadedFile(up_file, filename):
    saved_status = False
    if filename.strip=='':
        return saved_status

    try:
        up_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        saved_status = True
    except Exception as e:
        logger.debug('Cannot save Upladed file, e :' + e)
        saved_status = False
    return saved_status

def downloadAudioFileList():
    pass

def fileExists(folder, fileName):
    exists = os.path.exists(request.host_url + folder +'/' + fileName)
    return exists

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0')