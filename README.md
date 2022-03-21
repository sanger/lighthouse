# Lighthouse service

![CI](https://github.com/sanger/lighthouse/workflows/CI/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/sanger/lighthouse/branch/develop/graph/badge.svg)](https://codecov.io/gh/sanger/lighthouse)

A Flask Eve API to search through data provided by Lighthouse Labs. The data is populated in a
mongodb by the [crawler](https://github.com/sanger/crawler).

## Table of Contents

<!-- toc -->

- [A note on Docker](#a-note-on-docker)
- [Option A - using Docker](#option-a---using-docker)
  * [Requirements for Development](#requirements-for-development)
  * [Getting Started](#getting-started)
    + [Configuring the Environment](#configuring-the-environment)
    + [Setup Steps](#setup-steps)
  * [Running](#running)
  * [Testing](#testing)
- [Option B - without Docker](#option-b---without-docker)
  * [Requirements for Development](#requirements-for-development-1)
  * [Getting Started](#getting-started-1)
    + [Configuring the Environment](#configuring-the-environment-1)
    + [Setup Steps](#setup-steps-1)
  * [Running](#running-1)
  * [Testing](#testing-1)
    + [Testing Requirements](#testing-requirements)
    + [Running Tests](#running-tests)
- [Deployment](#deployment)
- [Routes](#routes)
- [Scheduled Jobs](#scheduled-jobs)
- [Miscellaneous](#miscellaneous)
  * [Type Checking](#type-checking)
  * [Troubleshooting](#troubleshooting)
    + [pyodbc Errors](#pyodbc-errors)
  * [Updating the Table of Contents](#updating-the-table-of-contents)

<!-- tocstop -->

## A note on Docker

Most of the notes in this readme are split into 'Option A - using Docker' and 'Option B - without Docker' sections.

Most of us have found we have to use Docker to develop locally due to an issue with 'pyodbc', which was ultimately caused by our HomeBrew installation not being in the root directory. These errors appeared once the SQL Server dependency was introduced to the project.

Details of the pyodbc error:

    ImportError: dlopen(/Users/.../.local/share/virtualenvs/lighthouse-e4xstWfp/lib/python3.8/site-packages/pyodbc.cpython-38-darwin.so, 2): Library not loaded: /usr/local/opt/unixodbc/lib/libodbc.2.dylib

This may be solved by recompiling pyodbc linked against your homebrew version of unixodbc.

https://github.com/mkleehammer/pyodbc/issues/681

If you still experience issues loading the MSSQL drivers themselves, you might need to use the docker container approach.

## Option A - using Docker

### Requirements for Development

A Docker installation is required.

### Getting Started

#### Configuring the Environment

Various environment variables are set in the docker-compose file.

#### Setup Steps

1. To start the database dependencies used by Lighthouse and also by Crawler
   there is a separate configuration for Docker Compose. This is shared with
   Crawler so if you start these dependencies here, there's no need to also
   attempt to do so in the Crawler repository. They are the same resources in
   both and the second one to be started will show exceptions about ports
   already being allocated:

        ./dependencies/up.sh

   When you want to shut the databases back down, you can do so with:

       ./dependencies/down.sh

### Running

1. Start the Lighthouse service specified in the `docker-compose.yml` from the
   root of the repository (this builds the docker image if it does not exist, then starts it up i.e. take care to delete old images or add --build):

        docker-compose up
        or
        docker-compose up --build

   This will keep running continuously in your terminal window, so to execute further commands you'll need
   to open a new terminal window or tab.

   To stop the lighthouse service container, press Ctrl-C back in the original window.

   If you would prefer it to run in background mode, add `-d` when starting, and stop the container
   using `docker-compose down`.

1. Start a bash session in the container with:

        docker exec -ti lighthouse_lighthouse_1 bash

   Warning! The names that Docker generates for containers might not be consistent over time. If this doesn't work for you,
   check the name of the container using `docker ps`.

   After this command you will be inside a bash session inside the container of lighthouse, and will have mounted all
   source code of the project from your hosting machine. The container will map your port 8000 with the port 8000 of
   Docker (configured in docker-compose.yml).

1. Now that you are inside the running container, initialize the MySQL and SQLServer development databases:

        python ./setup_sqlserver_test_db.py
        python ./setup_test_db.py

You should be able to access the app with a browser going to your local port 8000 (go to http://localhost:8000)

### Testing

Once you have got the lighthouse container running and started a bash session within it, you can run tests (flags are for verbose and exit early):

        python -m pytest -vx

## Option B - without Docker

### Requirements for Development

The following tools are required for development:

- python (use pyenv or something similar to install the python version specified in the `Pipfile`)
- mongodb
- MySQL
- Microsoft SQL Server

### Getting Started

#### Configuring the Environment

Non-sensitive environment variables can be stored in the `.flaskenv` file. These will be read
by the `python-dotenv` library when the app is run. Currently, these config variables are defined
there:

    FLASK_APP=lighthouse
    FLASK_RUN_HOST=0.0.0.0
    FLASK_RUN_PORT=8000
    FLASK_ENV=development
    EVE_SETTINGS=development.py

#### Setup Steps

- Use pyenv or something similar to install the version of python
  defined in the `Pipfile`:

        brew install pyenv
        pyenv install <python_version>
- Use pipenv to install the required python packages for the application and development:

        pipenv install --dev
- Sqlserver dependencies (assumes MacOS and homebrew)
  [Official instructions](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos?view=sql-server-ver15)
  You may experience difficulties if you have brew installed in your home directory. If this is the case, the Docker container approach may work better.

        brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
        brew update
        HOMEBREW_NO_ENV_FILTERING=1 ACCEPT_EULA=Y brew install msodbcsql17 mssql-tools unixodbc

- [Installing MongoDB](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/)

### Running

1. Enter the python virtual environment using:

        pipenv shell

1. Run the app using:

        flask run

### Testing

#### Testing Requirements

Verify the credentials for the required databases in the test settings file `lighthouse/config/test.py`.

#### Running Tests

Run the tests using pytest (flags are for verbose and exit early):

    python -m pytest -vx

A wrapper is provided with pipenv (look in the Pipfile's `[scripts]` block for more information):

    pipenv run test

**NB**: Make sure to be in the virtual environment (`pipenv shell`) before running the tests.

## Deployment

This project uses a Docker image as the unit of deployment. Update `.release-version` with
major/minor/patch. On merging a pull request into *develop* or *master*, a release will be created
along with the Docker image associated to that release.

NB:
When deploying a release you do not need to proceed it with a v as in Rails apps.
If the deployment fails you can use the following command to check why

    ssh dsm-01-uat.psd.sanger.ac.uk journalctl

You can filter by arbitrary time limits using the --since command e.g. with "1 hour ago"
You can also grep to limit by the release version you are looking for e.g. grep 2.21.1

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
