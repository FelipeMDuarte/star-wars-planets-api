# star-wars-planets-api
An API about the planets of the Star Wars universe.

## Getting Started

### Summary

The application is made in Python using the Flask framework and uses MongoDb as database.
You can run tests with Behave. The tests are found in the /features folder.
The application can be used localy or by Docker.
You can use Get, Post, Put and Delete requests to acess the api.

### Prerequisites

```
virtualenv
python 3.6
```

### Installing

Make a virtual env, activate it and execute `pip install -r requirements.txt`


### Configure

You have to set the following enviroment variables:
```
ENVIRONMENT=development
LOG_PATH=/var/log/app/
SERVICE_NAME=star-wars-planets-api
MONGO_URI=mongodb://<mongo_ip>:27017/star_wars_db
```
## Running the application

Basic run:

```
$ python app.py
```
This will execute the application in the port set on the app.py file.

## Running the test

Inside the virtual env and with the environment variables exported (They must have VALID values but not the true ones)
i.e.: MONGO_URI has to have "mongodb://"
Run BDD tests with behave:
```
$ behave
```
Mark unique scenarios that you wanna test with `@wip` as decorator.
Use -w for the run the unique scenario.

## Running with Docker

Build With Docker without env-file
```
$ docker build -t <Project-name> .
$ docker run -d -p 8000:80 <Project-name>
```
Build With Docker with an env-file
Attention: if you build with args, you can't overwrite the env-file when run it
```
$ docker build -t <Project-name> .
$ docker run -d -p 8000:80 --env-file path/your/file <Project-name>
```

If you wanna see it executes in the terminal change `-d` for `-it`

**ATTENTION**  
You have to change the ports and edit the file config.py

## Using the application
You will need to have a mongo database available and accessible.
After you run the application you can find its home page on "/"

To send get or post requests the endpoint is: `api/planets`
To send get unique, put or delete requests the endpoint is `api/planets/<id_or_name>`

Examples of the json bodies needed for each one can be found in the tests under the `features` folder
