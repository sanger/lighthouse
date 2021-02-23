#!/bin/bash

# Use this script to only install the required python packages depending on the environment.

if [[ ${ENV} == "test" ]]; then
    # if we want to run tests against the image, install all the dev dependencies
    echo "Installing packages required for testing"
    pipenv install --dev --ignore-pipfile
else
    # otherwise, "install packages exactly as specified in Pipfile.lock"
    #   https://pipenv.pypa.io/en/latest/advanced/#using-pipenv-for-deployments
    echo "Installing packages required for deployment"
    pipenv sync
fi
