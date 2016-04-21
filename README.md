# Twitter Monitor Service
Service for collecting statistics for tweets with keyword 'golang'

Application uses django and django rest framerowk.
Service is exposed on port 8000.
Functionality for twitter streaming API is run in seperate proccess. It uses django management command and is triggered inside docker startup script:
```
python3 manage.py start_streaming_twitter &
```

Service provides 3 endpoints:
- /twitter_stats/golang/   - responsible for returing number of tweets with 'golang' sent by users (per user) during stream monitoring

- /health/twitter/   - responsible for returning current twitter availability 

- /twitter_stats/  - responsible for returning number of all caught tweets with 'golang'


How to pass twitter authorization data?
- application expect that keys will be stored inside file: "secrets.py" with structure listed below.  
- they are not store inside repository or docker image. User have to create this file on his host and mount it using docker --volume(-v) option

secrets.py
```python

secrets = {
    'Consumer_Key': '<Consumer_Key>',
    'Consumer_Secret': '<Consumer_Secret>',
    'Access_Token': '<Access_Token>',
    'Access_Token_Secret': '<Access_Token_Secret>'}
```

How to run docker (with mounting secrets.py file and exposing needed ports) :
```
docker run -it --publish 8000:8000 --publish 9200:9200 --volume <full_path_to_your_version_of_secrets.py>:/srv/twitter_monitor_service/twitter_monitor_service/secrets.py zeemi/twitter_monitor_docker
```

(It may take a while after startup to collect tweets with expected keyword.)


Link do docker image:
https://hub.docker.com/r/zeemi/twitter_monitor_docker/

