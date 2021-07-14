# Lighthouse service

![CI](https://github.com/sanger/lighthouse/workflows/CI/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/sanger/lighthouse/branch/develop/graph/badge.svg)](https://codecov.io/gh/sanger/lighthouse)

A Flask Eve API to search through data provided by Lighthouse Labs. The data is populated in a
mongodb by the [crawler](https://github.com/sanger/crawler).

## Table of Contents

<!-- toc -->

- [Requirements for Development](#requirements-for-development)
- [Getting Started](#getting-started)
  * [Configuring the Environment](#configuring-the-environment)
  * [Setup Steps](#setup-steps)
- [Running](#running)
  * [Locally Using pipenv](#locally-using-pipenv)
  * [Using Docker](#using-docker)
- [Testing](#testing)
  * [Testing Requirements](#testing-requirements)
  * [Running Tests](#running-tests)
  * [Running tests with docker](#running-tests-with-docker)
- [Deployment](#deployment)
- [Routes](#routes)
- [Scheduled Jobs](#scheduled-jobs)
- [Miscellaneous](#miscellaneous)
  * [Type Checking](#type-checking)
  * [Troubleshooting](#troubleshooting)
    + [pyodbc Errors](#pyodbc-errors)
  * [Updating the Table of Contents](#updating-the-table-of-contents)

<!-- tocstop -->

## Requirements for Development

The following tools are required for development:

- python (use pyenv or something similar to install the python version specified in the `Pipfile`)
- mongodb
- MySQL
- Microsoft SQL Server

A `docker-compose.yml` file is available with separate `run` commands for each service if you prefer to run these
independently.

## Getting Started

### Configuring the Environment

Non-sensitive environmental variables can be stored in the `.flaskenv` file. These will be read
by the `python-dotenv` library when the app is run. Currently, these config variables are defined
there:

    FLASK_APP=lighthouse
    FLASK_RUN_HOST=0.0.0.0
    FLASK_RUN_PORT=8000
    FLASK_ENV=development
    EVE_SETTINGS=development.py

### Setup Steps

- Use pyenv or something similar to install the version of python
  defined in the `Pipfile`:

        brew install pyenv
        pyenv install <python_version>
- Use pipenv to install the required python packages for the application and development:

        pipenv install --dev
- Sqlserver dependencies (assumes MacOS and homebrew)
  [Official instructions](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos?view=sql-server-ver15)
  You may experience difficulties if you have brew installed in your home directory. If this is the case option B may work better.

        brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
        brew update
        HOMEBREW_NO_ENV_FILTERING=1 ACCEPT_EULA=Y brew install msodbcsql17 mssql-tools unixodbc
- (Optional) To start a Sqlserver container in local:

        docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=MyS3cr3tPassw0rd" -p 1433:1433 --name sqlserver \
        -h sql1 -d mcr.microsoft.com/mssql/server:2019-latest

- [Installing MongoDB](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/)

## Running

### Locally Using pipenv

1. Enter the python virtual environment using:

        pipenv shell

1. Run the app using:

        flask run

### Using Docker

1. Build the docker image using:

        docker build --tag lighthouse:develop .

1. Start the services specified in the `docker-compose.yml`:

        docker-compose up -d

    Or, you can start each individually using the instructions in the compose file.

1. Create a `.env` file which contains the line:

        LOCALHOST=host.docker.internal

1. Start the docker container and open a bash session in it with:

        docker run --env-file .env -p 8000:8000 -v $(pwd):/code -it --entrypoint bash lighthouse:develop

   After this command you will be inside a bash session inside the container of lighthouse, and will have mounted all
   source code of the project from your hosting machine The container will map your port 8000 with the port 8000 of
   Docker.

1. Once inside the docker container, run:

        pipenv install
        pipenv shell

1. Now that you are inside the virtual environment, initialize the development database for SQLServer:

        python ./setup_sqlserver_test_db.py
        python ./setup_test_db.py

1. Finally, start the app:

        flask run

   After this step you should be able to access the app with a browser going to your local port 8000 (go to http://localhost:8000)

## Testing

### Testing Requirements

Verify the credentials for the required databases in the test settings file `lighthouse/config/test.py`.

### Running Tests

Run the tests using pytest (flags are for verbose and exit early):

    python -m pytest -vx

A wrapper is provided with pipenv (look in the Pipfile's `[scripts]` block for more information):

    pipenv run test

**NB**: Make sure to be in the virtual environment (`pipenv shell`) before running the tests.

### Running tests with docker

If you are unable to run tests locally (because of `pyodbc` or other issues) then you can use the Docker Compose:

        docker compose up

Then in another terminal to get the container id:
        docker ps

You will then need to setup the MSSQL with:

        docker exec -ti <container_id for lighthouse> python ./setup_sqlserver_test_db.py

And the unified warehouse with:

        docker exec -ti <container_id for lighthouse> python ./setup_test_db.py

You can then run the tests inside the container:

        docker exec -ti <container_id for lighthouse> bash
        pipenv shell
        pipenv install
        python -m pytest

## Deployment

This project uses a Docker image as the unit of deployment. Update `.release-version` with
major/minor/patch. On merging a pull request into *develop* or *master*, a release will be created
along with the Docker image associated to that release.

## Routes

The service has the following routes:

        Endpoint                             Methods          Rule
    -----------------------------------  ---------------  ---------------------------------------------
    health_check                         GET              /health
    home                                 GET              /
    imports|item_lookup                  GET              /imports/<regex("[a-f0-9]{24}"):_id>
    imports|resource                     GET              /imports
    plates.create_plate_from_barcode     POST             /plates/new
    plates.find_plate_from_barcode       GET              /plates
    priority_samples|item_lookup         GET, PATCH, PUT  /priority_samples/<regex("[a-f0-9]{24}"):_id>
    priority_samples|item_post_override  POST             /priority_samples/<regex("[a-f0-9]{24}"):_id>
    priority_samples|resource            GET, POST        /priority_samples
    reports.create_report_endpoint       POST             /reports/new
    reports.delete_reports_endpoint      POST             /delete_reports
    reports.get_reports                  GET              /reports
    schema|item_lookup                   GET              /schema/<regex("[a-f0-9]{24}"):_id>
    schema|resource                      GET              /schema
    static                               GET              /static/<path:filename>

## Scheduled Jobs

This service runs a scheduled job to create a report (in `.xlsx` format) for use by the SSRs.

It is disabled by default. The config for the job can be found in `config/defaults.py`.

## Miscellaneous

### Type Checking

Type checking is done using mypy, to run it, execute:

    mypy .

### Troubleshooting

#### pyodbc Errors

If you experience:

    ImportError: dlopen(/Users/.../.local/share/virtualenvs/lighthouse-e4xstWfp/lib/python3.8/site-packages/pyodbc.cpython-38-darwin.so, 2): Library not loaded: /usr/local/opt/unixodbc/lib/libodbc.2.dylib

or similar when importing pyodbc, you may need to recompile pyodbc linked against your homebrew version of unixodbc.

https://github.com/mkleehammer/pyodbc/issues/681

If you still experience issues loading the MSSQL drivers themselves, you might need to use the docker container approach.

### Updating the Table of Contents

To update the table of contents after adding things to this README you can use the
[markdown-toc](https://github.com/jonschlinkert/markdown-toc) node module. To run:

    npx markdown-toc -i README.md
