# Use slim for a smaller image size and install only the required packages
FROM python:3.8-slim

# "Force the stdout and stderr streams to be unbuffered" - Docker logs to stdout and stderr so to prevent delay, do not
#   buffer message: https://docs.python.org/3/using/cmdline.html#cmdoption-u
ENV PYTHONUNBUFFERED 1

# This is required for Flask to know what app to start
ENV FLASK_APP lighthouse

# curl is required for the SQL Server, gnupg2 and build-essential are required to build unixodbc-dev
RUN apt-get update && apt-get install -y curl gnupg2 build-essential unixodbc-dev

# Install Microsoft SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y \
    msodbcsql17 \
    && rm -rf /var/lib/apt/lists/*

# Add a non-root user and update the PATH for the remaining build process
#   https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
RUN useradd --create-home lighthouse
ENV PATH "$PATH:/home/lighthouse/.local/bin"

# Change the working directory for all proceeding operations
#   https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#workdir
WORKDIR /home/lighthouse/app

# Create and set the ownership of the data directory - currently in the .dockerignore file
RUN mkdir -p data/reports && chown lighthouse:lighthouse data/reports

# Use the data directory as a volume
VOLUME data/reports

# Run the rest of the commands as lighthouse user
USER lighthouse

RUN pip install --user pipenv

# "items (files, directories) that do not require ADD’s tar auto-extraction capability, you should always use COPY."
#   https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#add-or-copy
COPY --chown=lighthouse Pipfile ./
COPY --chown=lighthouse Pipfile.lock ./

# Install the required python packages
RUN pipenv sync --dev

# Copy all the source to the image
COPY --chown=lighthouse . .

# https://docs.docker.com/engine/reference/builder/#healthcheck
HEALTHCHECK --interval=1m --timeout=3s \
    CMD curl -f http://localhost:8000/health || exit 1

# "The best use for ENTRYPOINT is to set the image’s main command, allowing that image to be run as though it was that
#   command (and then use CMD as the default flags)."
#   https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#entrypoint
ENTRYPOINT ["pipenv", "run", "flask"]
CMD ["run", "--host", "0.0.0.0", "--port", "8000"]
