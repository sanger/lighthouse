# Use slim for a smaller image size and install only the required packages
FROM python:3.13-slim

# Use the following on M1; for odbc connection to mssql.
# FROM --platform=linux/amd64 python:3.8-slim-buster

# > Setting PYTHONUNBUFFERED to a non empty value ensures that the python output is sent straight to
# > terminal (e.g. your container log) without being first buffered and that you can see the output
# > of your application (e.g. django logs) in real time.
#   https://stackoverflow.com/a/59812588
#   https://docs.python.org/3/using/cmdline.html#cmdoption-u
ENV PYTHONUNBUFFERED 1

# curl is required for the SQL Server; gnupg2 and build-essential are required to build unixodbc-dev
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    curl \
    gnupg2 \
    unixodbc-dev

# Install the Microsoft ODBC driver for SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18
RUN apt-get install -y unixodbc-dev

# Install the package manager - pipenv
RUN pip install --upgrade pip && \
    pip install --no-cache-dir pipenv

# Change the working directory for all proceeding operations
#   https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#workdir
WORKDIR /code

# "items (files, directories) that do not require ADD’s tar auto-extraction capability, you should always use COPY."
#   https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#add-or-copy
COPY Pipfile .
COPY Pipfile.lock .

# Install both default and dev packages so that we can run the tests against this image
RUN pipenv sync --dev --system && \
    pipenv --clear

# Copy all the source to the image
COPY . .

# "The best use for ENTRYPOINT is to set the image’s main command, allowing that image to be run as though it was that
#   command (and then use CMD as the default flags)."
#   https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#entrypoint
ENTRYPOINT ["flask"]
CMD ["run"]


# https://docs.docker.com/engine/reference/builder/#healthcheck
HEALTHCHECK --interval=30s --timeout=5s \
    CMD curl -f http://localhost:8000/health || exit 1
