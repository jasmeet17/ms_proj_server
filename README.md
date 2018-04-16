# Master Project


This is a backend code for the project "Improving Accent and pronunciation"


### To run the app

Clone the project
```sh
$ git clone https://github.com/jasmeet17/ms_proj_server
$ cd ms_proj_server
```

To run the application; first store all your audio files in the Amazon S3 cloud bucket and get access key and secret key. Store the keys inside the credentials.json and keep it inside ms_proj_server/code/

To run the server you need Docker install. Run the docker from your machine. To run python server use:
```sh
$ docker run -p 5000:5000 -e API_TEST=true -e APP_NAME=app.py -v $(pwd)/code:/data/:rw --name test_py python-sound
```

To run files locally use:
```sh
docker run --rm -e LIBROSA_TEST=true -e APP_NAME=differentiate.py -v $(pwd)/code:/data/:rw python-sound
```

And you can access the server from localhost:5000
