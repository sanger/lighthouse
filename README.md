# Lighthouse

A Flask Eve API to search through data provided by Lighthouse Labs. The data is populated in a
mongodb by the [crawler](https://github.com/sanger/crawler).

The services has the following routes:

    Endpoint                          Methods  Rule
    --------------------------------  -------  ------------------------------------
    centres|item_lookup               GET      /centres/<regex("[a-f0-9]{24}"):_id>
    centres|resource                  GET      /centres
    health_check                      GET      /health
    home                              GET      /
    imports|item_lookup               GET      /imports/<regex("[a-f0-9]{24}"):_id>
    imports|resource                  GET      /imports
    media                             GET      /media/<regex("[a-f0-9]{24}"):_id>
    plates.create_plate_from_barcode  POST     /plates/new
    samples|item_lookup               GET      /samples/<regex("[a-f0-9]{24}"):_id>
    samples|resource                  GET      /samples
    schema|item_lookup                GET      /schema/<regex("[a-f0-9]{24}"):_id>
    schema|resource                   GET      /schema
    static                            GET      /static/<path:filename>

## Requirements

* [pyenv](https://github.com/pyenv/pyenv)
* [pipenv](https://pipenv.pypa.io/en/latest/)
* mongodb

## Setup

* Use pyenv or something similar to install the version of python
defined in the `Pipfile`:
  1. `brew install pyenv`
  2. `pyenv install <python_version>`
* Use pipenv to install python packages: `brew install pipenv`
* To install the required packages (and dev packages) run: `pipenv install --dev`

## Running

1. Create a `.env` file with the following contents (or use `.env.example` - rename to `.env`):
    * `BARACODA_HOST=127.0.0.1`
    * `BARACODA_PORT=5001`
    * `FLASK_APP=lighthouse`
    * `FLASK_ENV=development`
    * `MONGO_DBNAME=crawlerDevelopmentDB`
    * `MONGO_HOST=127.0.0.1`
    * `MONGO_PASSWORD=`
    * `MONGO_PORT=27017`
    * `MONGO_USERNAME=`
    * `SLACK_API_TOKEN=xoxb`
    * `SLACK_CHANNEL_ID=C`
    * `SS_API_KEY=development`
    * `SS_HOST=localhost:3000`
    * `SS_UUID_PLATE_PURPOSE=11111111`
    * `SS_UUID_STUDY=12345`

1. Enter the python virtual environment using:

        pipenv shell

1. Run the app using:

        flask run

__NB:__ When adding or changing environmental variables, remember to exit and re-enter the virtual
environment.

## Testing

1. Verify the credentials for your database in the settings file 'tests/config.py'
1. Run the tests using pytest (flags are for verbose, exit early and capture output):

        python -m pytest -vsx

__NB__: Make sure to be in the virtual environment (`pipenv shell`) before running the tests:

## Type checking

Type checking is done using mypy, to run it, execute `mypy .`

## Contributing

This project uses [black](https://github.com/psf/black) to check for code format, the use it run:
`black .`
