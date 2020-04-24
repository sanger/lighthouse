from os import getenv

BARACODA_HOST = getenv("BARACODA_HOST")
BARACODA_PORT = getenv("BARACODA_PORT")

REQUIRED_CONFIG = ("BARACODA_HOST", "BARACODA_PORT")

for config in REQUIRED_CONFIG:
    if not eval(config):
        raise ValueError(f"{config} required for Flask application")
