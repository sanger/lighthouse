FROM python:3.8

# Needed for something...
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install pipenv

WORKDIR /code

COPY Pipfile /code/
COPY Pipfile.lock /code/

# Install both default and dev packages so that we can run the tests against this image
RUN pipenv install --dev --ignore-pipfile --system --deploy

ADD . /code/

# As described in https://pythonspeed.com/articles/gunicorn-in-docker/
CMD ["gunicorn", "-b", "0.0.0.0:8000", "--workers=2", "--threads=4", "--worker-class=gthread", "--timeout", "0", "--log-level", "DEBUG", "--worker-tmp-dir", "/dev/shm", "lighthouse:create_app()"]
