import copy
import os

import pytest  # type: ignore
import responses  # type: ignore

from lighthouse import create_app

from .data.fixture_data import CENTRES, SAMPLES, SAMPLES_DECLARATIONS


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
def samples_declarations(app):
    with app.app_context():
        samples_declarations_collections = app.data.driver.db.samples_declarations
        _ = samples_declarations_collections.insert_many(SAMPLES_DECLARATIONS)

    yield copy.deepcopy(SAMPLES_DECLARATIONS)

    # clear up after the fixture is used
    with app.app_context():
        samples_declarations_collections.delete_many({})


@pytest.fixture
def lots_of_samples(app):
    num_samples = 1000
    samples = []
    i = 0
    while i < num_samples:
        samples.append(
            {
                "root_sample_id": f"MCM{i}",
                "value_in_sequencing": "Yes",
                "declared_at": "2013-04-06T10:29:13",
            }
        )
        i = i + 1

    with app.app_context():
        samples_declarations_collections = app.data.driver.db.samples_declarations

    yield copy.deepcopy(samples)

    # clear up after the fixture is used
    with app.app_context():
        samples_declarations_collections.delete_many({})


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
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps
