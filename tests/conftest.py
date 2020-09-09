import copy
import os
import json

import pytest
import responses  # type: ignore
from http import HTTPStatus


from lighthouse import create_app

from .data.fixture_data import (
    CENTRES,
    SAMPLES,
    SAMPLES_DECLARATIONS,
    LOTS_OF_SAMPLES,
    LOTS_OF_SAMPLES_DECLARATIONS_PAYLOAD,
    MULTIPLE_ERRORS_SAMPLES_DECLARATIONS,
    SAMPLES_NO_DECLARATION
)


@pytest.fixture
def app():
    # set the 'EVE_SETTINGS' env variable to easily switch to the testing environment when creating
    #   an app
    os.environ["EVE_SETTINGS"] = "test.py"

    app = create_app()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def centres(app):
    with app.app_context():
        centres_collection = app.data.driver.db.centres
        _ = centres_collection.insert_many(CENTRES)

    #  yield a copy so that the test change it however it wants
    yield copy.deepcopy(CENTRES)

    # clear up after the fixture is used
    with app.app_context():
        centres_collection.delete_many({})


@pytest.fixture
def empty_data_when_finish(app):
    yield

    with app.app_context():
        mydb = app.data.driver.db
        mydb.samples.delete_many({})
        mydb.samples_declarations.delete_many({})
        mydb.centres.delete_many({})


@pytest.fixture
def samples_declarations(app):
    with app.app_context():
        samples_declarations_collections = app.data.driver.db.samples_declarations
        _ = samples_declarations_collections.insert_many(SAMPLES_DECLARATIONS)

    yield copy.deepcopy(SAMPLES_DECLARATIONS)

    # clear up after the fixture is used
    with app.app_context():
        samples_declarations_collections.delete_many({})


@pytest.fixture
def lots_of_samples_declarations_payload(app):
    yield copy.deepcopy(LOTS_OF_SAMPLES_DECLARATIONS_PAYLOAD)


@pytest.fixture
def multiple_errors_samples_declarations_payload(app):
    yield copy.deepcopy(MULTIPLE_ERRORS_SAMPLES_DECLARATIONS)


@pytest.fixture
def lots_of_samples(app):
    with app.app_context():
        samples_collections = app.data.driver.db.samples
        _ = samples_collections.insert_many(LOTS_OF_SAMPLES)

    yield copy.deepcopy(LOTS_OF_SAMPLES)

    # clear up after the fixture is used
    with app.app_context():
        samples_collections.delete_many({})


@pytest.fixture
def samples(app):
    with app.app_context():
        samples_collection = app.data.driver.db.samples
        _ = samples_collection.insert_many(SAMPLES)

    #  yield a copy of that the test change it however it wants
    yield copy.deepcopy(SAMPLES)

    # clear up after the fixture is used
    with app.app_context():
        samples_collection.delete_many({})

@pytest.fixture
def samples_no_declaration(app):
    with app.app_context():
        samples_collection = app.data.driver.db.samples
        _ = samples_collection.insert_many(SAMPLES_NO_DECLARATION)

    #  yield a copy of that the test change it however it wants
    yield copy.deepcopy(SAMPLES_NO_DECLARATION)

    # clear up after the fixture is used
    with app.app_context():
        samples_collection.delete_many({})

@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def labwhere_samples_simple(app, mocked_responses):
    labwhere_url = f"http://{app.config['LABWHERE_URL']}/api/labwares/searches"

    body = json.dumps([{"barcode": "123", "location": {"barcode": "4567"}}])
    mocked_responses.add(
        responses.POST, labwhere_url, body=body, status=HTTPStatus.OK,
    )

@pytest.fixture
def labwhere_samples_multiple(app, mocked_responses):
    labwhere_url = f"http://{app.config['LABWHERE_URL']}/api/labwares/searches"

    body = json.dumps([
        {"barcode": "123", "location": {"barcode": "4567"}},
        {"barcode": "456", "location": {"barcode": "1234"}},
        {"barcode": "789", "location": {}}
    ])
    mocked_responses.add(
        responses.POST, labwhere_url, body=body, status=HTTPStatus.OK,
    )

@pytest.fixture
def labwhere_samples_error(app, mocked_responses):
    labwhere_url = f"http://{app.config['LABWHERE_URL']}/api/labwares/searches"

    body = json.dumps([])
    mocked_responses.add(
        responses.POST, labwhere_url, body=body, status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )
