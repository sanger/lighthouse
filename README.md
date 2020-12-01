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
- Use pipenv to install python packages:
  1. `brew install pipenv`
- To install the required packages (and dev packages) run the following:
  1. `pipenv shell`
  2. `pipenv install --dev` (without the --dev you don't get pytest, mypy etc.)
- Sqlserver dependencies (assumes MacOS and homebrew)
  [Official instructions](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos?view=sql-server-ver15)
  1. You may experience difficulties if you have brew installed in your home directory. If this is the case option B may work better.
  2. `brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release`
  3. `brew update`
  4. `HOMEBREW_NO_ENV_FILTERING=1 ACCEPT_EULA=Y brew install msodbcsql17 mssql-tools unixodbc`
- (Optional) To start a Sqlserver container in local:
  1. `docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=MyS3cr3tPassw0rd" -p 1433:1433 --name sqlserver -h sql1 -d mcr.microsoft.com/mssql/server:2019-latest`

- [Installing MongoDB](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/)

## Running

Create a `.env` file with the following contents (or use `.env.example` - rename to `.env`):

    - `FLASK_APP=lighthouse`
    - `FLASK_ENV=development`
    - `EVE_SETTINGS=development.py`

Option A (in local):

1. Enter the python virtual environment using:

        pipenv shell

2. Run the app using:

        flask run

**NB:** When adding or changing environmental variables, remember to exit and re-enter the virtual
environment.

Option B (in Docker):

1. Build the docker image using:

        docker build -t lighthouse:develop .

2. Sql server

        docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=MyS3cr3tPassw0rd" \
        -p 1433:1433 --name sql1 -h sql1 \
        -d mcr.microsoft.com/mssql/server:2019-latest

3. Ensure your .env file contains the line

        LOCALHOST=host.docker.internal

3. Start the docker container and open a bash session in it with:

        docker run --env-file .env -p 5000:5000 -v `pwd`:/code -it lighthouse:develop bash

   After this command you will be inside a bash session inside the container of lighthouse, and will have mounted all
   source code of the project from your hosting machine (You can replace `pwd` with your actual directory).
   The container will map your port 5000 with the port 5000 of Docker.

4. Inside the docker container, you may also need to run

        pipenv install
        pipenv shell

5. Initialize the development database for sqlserver inside `pipenv shell`:

        python ./setup_sqlserver_test_db.py
        python ./setup_test_db.py


6. Now that you are inside the container, start the app in port 5000 of Docker using:

        flask run -h 0.0.0.0

   After this step you should be able to access the app with a browser going to your local port 5000 (go to http://localhost:5000)

## Testing

1. Verify the credentials for your database in the settings file 'lighthouse/config/test.py'
1. Run the tests using pytest (flags are for verbose, exit early and capture output):

        python -m pytest -vsx

**NB**: Make sure to be in the virtual environment (`pipenv shell`) before running the tests:

## Type checking

Type checking is done using mypy, to run it, execute `mypy .`

## Troubleshooting

If you experience `ImportError: dlopen(/Users/.../.local/share/virtualenvs/lighthouse-e4xstWfp/lib/python3.8/site-packages/pyodbc.cpython-38-darwin.so, 2): Library not loaded: /usr/local/opt/unixodbc/lib/libodbc.2.dylib` or
similar when importing pyodbc you may need to recompile pyodbc linked against your homebrew version of unixodbc.

https://github.com/mkleehammer/pyodbc/issues/681

However, following this I still had issues loading the MSSQL drivers themselves, as they didn't seem to like
the homebrew install path in my home directory. In this case, I ended up needing to use the docker container
approach.

## Contributing

This project uses [black](https://github.com/psf/black) to check for code format, the use it run:
`black .`
