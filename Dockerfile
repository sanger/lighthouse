FROM python:3.8

# Needed for something...
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install pipenv

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get -y update
RUN apt-get -y install telnet
RUN ACCEPT_EULA=Y apt-get -y install msodbcsql17
# optional: for bcp and sqlcmd
RUN ACCEPT_EULA=Y apt-get -y install mssql-tools
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

# optional: for unixODBC development headers
RUN apt-get install -y unixodbc-dev
# optional: kerberos library for debian-slim distributions
#sudo apt-get install libgssapi-krb5-2


WORKDIR /code

COPY Pipfile /code/
COPY Pipfile.lock /code/

# Remember to rollback line to this:
# Install both default and dev packages so that we can run the tests against this image
RUN pipenv install --dev --ignore-pipfile --system --deploy

ADD . /code/

# As described in https://pythonspeed.com/articles/gunicorn-in-docker/
CMD ["gunicorn", "-b", "0.0.0.0:8000", "--workers=2", "--threads=4", "--worker-class=gthread", "--preload", "--timeout", "0", "--log-level", "DEBUG", "--worker-tmp-dir", "/dev/shm", "lighthouse:create_app()"]
