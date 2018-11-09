# star-wars-planets-api
An API about the planets of the Star Wars movies.

# Mvp Autometadata Orchestrator Service

Orchestrator to receive post from mvp autometadata ingest and send posts to thumb generator and autometadata job data

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

#### Linux/Mac OS
```
virtualenv
python 3.6
```

### Installing

```
$ cd minimal-template
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip  install -r requirements.txt
```

End with an example of getting some data out of the system or using it for a little demo

### Configure

Change the value of the variable `SERVICE_NAME` to the name of the new service:  

```
ENVIRONMENT=production
LOG_PATH=/var/log/app/
SERVICE_NAME=mvp-autometadata-orch
```
## Running the application

Basic run:

```
$ python app.py
```

Build With Docker without env-file
```
$ docker build -t <Project-name> .
$ docker run -d -p 8000:80 <Project-name>
```
Build With Docker with an env-file (you can build with staging, dev or production) eg: APP_ENVIROMENT=dev
Attention: if you build with args, you can't overwrite the env-file when run it
```
$ docker build -t <Project-name> --build-arg APP_ENVIRONMENT=<stg|dev|prd> .
$ docker run -d -p 8000:80 <Project-name>
```
Run docker using env file if you don't specified it in build definition
```
$ docker run -d -p 8000:80 --env-file path/your/file <Project-name>
```

**ATTENTION**  
You have to change the ports and edit the file config.py
You must add the config envirmonment variables to .gitlab-ci.yml


## Running the test

run BDD tests with behave:
```
$ behave
```
Use -w for the run the unique scenario.


## Built With

* [Flask](http://flask.pocoo.org/) - The web framework used


## Release History  
* 1.0.0
  * start of the project
