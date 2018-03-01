import boto3
import botocore
import csv
import json
import logging

CRED_FILE = 'credentials.json'
BUCKET = 'accent-audio-files'
AUDIO_FOLDER = 'audio_files/'
TEMP_FOLDER = 'static/tmp/'
LOG_FOLDER = 'static/logs/'

import sys

class AwsBucket(object):
    """AwsBucket makes connection with the AWS for S3 object"""
    def __init__(self):
        super(AwsBucket, self).__init__()
        self.connectAws()

    """connectAws makes the connection with the Bucket"""
    def connectAws(self):
        read_creds = open(CRED_FILE, 'r')
        creds = json.load(read_creds)

        ACCESS_KEY = creds['ACCESS_KEY']
        SECRET_KEY = creds['SECRET_KEY']

        read_creds.close()

        self.__s3 = boto3.resource('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
        self.__my_bucket = self.__s3.Bucket(BUCKET)

    """returns file(.flac or other file ) from the bucket else returns False"""
    def getFile(self, key):
        if key.strip() == '':
            return False

        temp_file = ''

        try:
            temp_file = self.__s3.Object(BUCKET, AUDIO_FOLDER + key).get()['Body'].read()
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "NoSuchKey":
                print("The object does not exist.")
            else:
                print(e.response['Error'])
                return False

        return temp_file

    """Saved the requested file and return True for successful save."""
    def downloadFile(self, key):
        downloaded = False

        if key.strip()=='':
            return downloaded

        try:
            self.__my_bucket.download_file(AUDIO_FOLDER + key, TEMP_FOLDER + key)
            downloaded = True
        except botocore.exceptions.ClientError as e:
            downloaded = False
            if e.response['Error']['Code'] == "NoSuchKey":
                # logger.debug("The object does not exist. e:" + e)
                pass
            else:
                pass
                # logger.debug(e.response['Error'])
                # return downloaded
            return e

        return downloaded

# if __name__ == '__main__':
#     aws_bucket = AwsBucket()