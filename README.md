# Lighthouse

![CI python](https://github.com/sanger/lighthouse/workflows/CI%20python/badge.svg)
![CI docker](https://github.com/sanger/lighthouse/workflows/CI%20docker/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/sanger/lighthouse/branch/develop/graph/badge.svg)](https://codecov.io/gh/sanger/lighthouse)

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
    reports.create_report             POST     /reports/new
    reports.get_reports               GET      /reports
    samples|item_lookup               GET      /samples/<regex("[a-f0-9]{24}"):_id>
    samples|resource                  GET      /samples
    schema|item_lookup                GET      /schema/<regex("[a-f0-9]{24}"):_id>
    schema|resource                   GET      /schema
    static                            GET      /static/<path:filename>

## Requirements

- [pyenv](https://github.com/pyenv/pyenv)
- [pipenv](https://pipenv.pypa.io/en/latest/)
- mongodb

## Setup

- Use pyenv or something similar to install the version of python
  defined in the `Pipfile`:
  1. `brew install pyenv`
  2. `pyenv install <python_version>`
- Use pipenv to install python packages: `brew install pipenv`
- To install the required packages (and dev packages) run: `pipenv install --dev`

## Running

1. Create a `.env` file with the following contents (or use `.env.example` - rename to `.env`):

    - `FLASK_APP=lighthouse`
    - `FLASK_ENV=development`
    - `EVE_SETTINGS=development.py`

1. Enter the python virtual environment using:

        pipenv shell

1. Run the app using:

        flask run

**NB:** When adding or changing environmental variables, remember to exit and re-enter the virtual
environment.

## Testing

1. Verify the credentials for your database in the settings file 'tests/config.py'
1. Run the tests using pytest (flags are for verbose, exit early and capture output):

        python -m pytest -vsx

**NB**: Make sure to be in the virtual environment (`pipenv shell`) before running the tests:

## Type checking

Type checking is done using mypy, to run it, execute `mypy .`

## Contributing

This project uses [black](https://github.com/psf/black) to check for code format, the use it run:
`black .`
