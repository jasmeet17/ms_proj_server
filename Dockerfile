FROM nutzio/librosa-env
MAINTAINER Jasmeet

ADD ./requirements.txt /requirements.txt

# Environment Variables for exposing port
ENV BIND_PORT 5000

# Environment Variables for Development
ENV APP_NAME app.py
ENV LIBROSA_TEST false
ENV API_TEST false
ENV FILE_1 ability.flac
ENV FILE_2 ability.flac

WORKDIR /data
VOLUME /data


# Update tool for alpine ; required by requirements
RUN apk update

# RUN apk add <package-1> <package-2> <package-3> . . .
RUN apk add freetype-dev gcc alpine-sdk

# install dependencies
RUN pip install -r /requirements.txt

# Expose the port
#EXPOSE $BIND_PORT
EXPOSE 5000

# run CMD based on flags for development
CMD sh -c 'if [ "$LIBROSA_TEST"=true ]; then python3 $APP_NAME $FILE_1 $FILE_2; fi'
# CMD sh -c 'if [ "$API_TEST"=true ]; then export FLASK_DEBUG=1; fi'
# CMD sh -c 'if [ "$API_TEST"=true ]; then python3 $APP_NAME; fi'
# CMD sh -c 'python3 $APP_NAME;'

#docker run --rm -e LIBROSA_TEST=true -e APP_NAME=differentiate.py -v $(pwd)/code:/data/:rw python-sound
#docker run --rm -e API_TEST=true -e APP_NAME=app.py -v $(pwd)/code:/data/:rw python-sound-test
#docker run -id -p 5000:5000 -e API_TEST=true -e APP_NAME=app.py -v $(pwd)/code:/data/:rw --name test_py python-sound
#docker run -p 5000:5000 -e API_TEST=true -e APP_NAME=app.py -v $(pwd)/code:/data/:rw --name test_py python-sound
#docker stop test_py && docker rm test_py
#docker run -e LIBROSA_TEST=true -e APP_NAME=differentiate.py -e FILE_1=benefit.flac -e FILE_2=benefit.m4a -v $(pwd)/code:/data/:rw python-sound
